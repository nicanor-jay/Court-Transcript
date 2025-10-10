# pylint: disable=use-dict-literal, too-many-branches, too-many-return-statements
"""
UK Judiciary Web Scraper - Judges Only (Simplified Selenium)
Scrapes judiciary.uk and extracts only real judges.
"""

from os import mkdir
import json
from datetime import datetime
from typing import List, Dict, Optional
import re
from tempfile import mkdtemp

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

TITLES = [
    "The Right Honourable Lord Justice",
    "The Right Honourable Lady Justice",
    "The Honourable Mr Justice",
    "The Honourable Mrs Justice",
    "The Honourable Judge",
    "District Judge (MC)", "District Judge",
    "Lord Chief Justice",
    "Lord Justice", "Lady Justice",
    "His Honour Judge", "Her Honour Judge",
    "Mr Justice", "Mrs Justice",
    "Tribunal Judge",
    "His Honour", "Her Honour",
    "Lord", "Lady", "Sir", "Dame",
    "The",
    "Mr", "Mrs", "Miss", "Ms",
    "Dr", "Professor",
    "Judge", "HHJ", "DHJ", "DJ",
]

POST_NOMINALS = ["KC", "QC", "CBE", "OBE", "MBE", "JP"]

# Prefixes that indicate multiword surnames
SURNAME_PREFIXES = ["van", "van der", "van den",
                    "de", "de la", "du", "von", "von der"]


def parse_date(text: str) -> Optional[str]:
    """Parse a date string into ISO format if possible."""
    if not text:
        return None
    text = text.strip()

    match = re.search(r"\b\d{2}[-/\.]\d{2}[-/\.]\d{2,4}\b", text)
    if match:
        raw_date = match.group(0)
        formats = [
            "%d-%m-%y", "%d-%m-%Y",
            "%d/%m/%y", "%d/%m/%Y",
            "%d.%m.%y", "%d.%m.%Y",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(raw_date, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

    formats = [
        "%d %B %Y", "%d %b %Y",
        "%Y-%m-%d", "%B %Y", "%b %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def parse_name(full: str) -> Dict[str, Optional[str]]:
    """Split judge full name into components."""
    result = dict(title=None, first_name=None,
                  middle_name=None, last_name=None)
    if not full:
        return result

    full_lower = full.lower()
    matched_title = None
    remaining_text = full

    for title in TITLES:
        title_lower = title.lower()
        if full_lower.startswith(title_lower + " ") or full_lower == title_lower:
            matched_title = title
            remaining_text = full[len(title):].strip()
            break

    result["title"] = matched_title
    full = remaining_text

    for post_nom in POST_NOMINALS:
        post_nom_lower = post_nom.lower()
        if full.lower().endswith(" " + post_nom_lower):
            full = full[: -len(post_nom) - 1].strip()

    parts = full.split()
    if not parts:
        return result
    if len(parts) == 1:
        result["last_name"] = parts[0]
        return result

    surname_start_idx = None
    for prefix in sorted(SURNAME_PREFIXES, key=len, reverse=True):
        prefix_parts = prefix.split()
        for i in range(len(parts) - len(prefix_parts)):
            candidate = " ".join(parts[i:i+len(prefix_parts)]).lower()
            if candidate == prefix.lower():
                surname_start_idx = i
                break
        if surname_start_idx is not None:
            break

    if surname_start_idx is not None:
        if surname_start_idx == 0:
            result["last_name"] = " ".join(parts[surname_start_idx:])
        else:
            result["first_name"] = parts[0]
            if surname_start_idx > 1:
                result["middle_name"] = " ".join(parts[1:surname_start_idx])
            result["last_name"] = " ".join(parts[surname_start_idx:])
    else:
        if len(parts) == 2:
            result["first_name"], result["last_name"] = parts
        else:
            result["first_name"], result["last_name"] = parts[0], parts[-1]
            result["middle_name"] = " ".join(parts[1:-1])
    return result


def looks_like_judge(text: str) -> bool:
    """Return True if text looks like a judge name."""
    if not text:
        return False
    text_lower = text.lower()

    exclusions = [
        "the black country", "the midlands", "the north", "the south",
        "the east", "the west", "the city", "the county", "the district",
        "the region", "the area", "the circuit", "the division"
    ]
    if any(text_lower.startswith(excl) for excl in exclusions):
        return False

    if not any(text_lower.startswith(t.lower() + " ") for t in TITLES):
        return False

    for title in TITLES:
        title_lower = title.lower()
        if text_lower.startswith(title_lower + " "):
            remainder = text[len(title):].strip()
            if not remainder or len(remainder.split()) == 0:
                return False
            words = remainder.split()
            if len(words) >= 1:
                location_words = {"country", "region", "area", "circuit", "division",
                                  "midlands", "north", "south", "east", "west", "city",
                                  "county", "district", "wales", "scotland", "england", "ireland"}
                if all(w.lower() in location_words for w in words):
                    return False
            return True

    return False


def scrape_page(driver, url: str) -> List[Dict]:
    """Scrape all judges from one URL."""
    judges = []
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
    except:
        return judges

    tables = driver.find_elements(By.TAG_NAME, "table")

    for table in tables:
        rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cells = [c.text.strip()
                     for c in row.find_elements(By.TAG_NAME, "td")]

            if not cells or not cells[0]:
                continue

            full_name = cells[0]
            if not looks_like_judge(full_name):
                continue

            date_val = next((parse_date(c)
                            for c in cells[1:] if parse_date(c)), None)
            parsed = parse_name(full_name)

            judges.append({
                "source_url": url,
                "full_name": full_name,
                "title": parsed["title"],
                "first_name": parsed["first_name"],
                "middle_name": parsed["middle_name"],
                "last_name": parsed["last_name"],
                "appointment_date": date_val,
            })

    return judges


def extract_titles(judges: List[Dict]) -> List[Dict]:
    """Extract unique titles from judges and create title records."""
    seen_titles = {judge["title"] for judge in judges if judge.get("title")}
    sorted_titles = sorted(seen_titles)
    return [{"title_id": idx, "title_name": title}
            for idx, title in enumerate(sorted_titles, start=1)]


def add_title_ids(judges: List[Dict], titles: List[Dict]) -> None:
    """Add title_id to each judge based on the titles lookup."""
    title_map = {t["title_name"]: t["title_id"] for t in titles}
    for judge in judges:
        title_name = judge.get("title")
        judge["title_id"] = title_map.get(title_name) if title_name else None


def normalise_judge(judge: Dict) -> Dict:
    """Convert None values to empty strings for database-safe JSON."""
    for key in ["first_name", "middle_name", "last_name"]:
        if judge.get(key) is None:
            judge[key] = ''
    return judge


def judge_main():
    """Main entry point."""
    base_url = (
        "https://www.judiciary.uk/about-the-judiciary/who-are-the-judiciary/"
        "list-of-members-of-the-judiciary/"
    )

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver")
    driver = Chrome(
        service=service,
        options=chrome_options)

    try:
        driver.get(base_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )

        link_elements = driver.find_elements(
            By.CSS_SELECTOR, 'a[href*="list-of-members"]')
        links = [elem.get_attribute(
            "href") for elem in link_elements if elem.get_attribute("href")]

        links = [
            f"https://www.judiciary.uk{l}" if l.startswith("/") else l for l in links]

        all_judges = []
        if links:
            for link in links:
                all_judges.extend(scrape_page(driver, link))
        else:
            all_judges.extend(scrape_page(driver, base_url))

    finally:
        driver.quit()

    titles = extract_titles(all_judges)
    add_title_ids(all_judges, titles)
    normalised_judges = [normalise_judge(j) for j in all_judges]

    with open("/tmp/titles_data.json", "w", encoding="utf-8") as f:
        json.dump(titles, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(titles)} unique titles -> titles_data.json")

    with open("/tmp/judges_data.json", "w", encoding="utf-8") as f:
        json.dump(normalised_judges, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(normalised_judges)} judges -> judges_data.json")


if __name__ == "__main__":
    judge_main()
