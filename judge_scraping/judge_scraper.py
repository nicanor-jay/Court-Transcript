#pylint: disable=use-dict-literal, too-many-branches, too-many-return-statements
"""
UK Judiciary Web Scraper - Judges Only
Scrapes judiciary.uk and extracts *only* real judges.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
import re
from playwright.sync_api import sync_playwright

# Judicial titles (longest first to avoid partial matches)
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

# Postnominal titles to strip from the end
POST_NOMINALS = ["KC", "QC", "CBE", "OBE", "MBE", "JP"]

# Prefixes that indicate multiword surnames
SURNAME_PREFIXES = ["van", "van der", "van den", "de", "de la", "du", "von", "von der"]


def parse_date(text: str) -> Optional[str]:
    """Parse a date string into ISO format if possible."""
    if not text:
        return None
    text = text.strip()

    # Regex to detect common numeric formats (e.g. 14-05-18, 14/05/2018)
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
    result = dict(title=None, first_name=None, middle_name=None, last_name=None)
    if not full:
        return result

    # Case-insensitive title matching - try longest matches first
    full_lower = full.lower()
    matched_title = None
    remaining_text = full

    for title in TITLES:
        title_lower = title.lower()
        # Check if starts with this title followed by space or end of string
        if full_lower.startswith(title_lower + " ") or full_lower == title_lower:
            matched_title = title  # Keep original casing for storage
            remaining_text = full[len(title):].strip()
            break

    result["title"] = matched_title

    # Work with the remaining text after title
    full = remaining_text

    # Case-insensitive post-nominal removal
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

    # Case-insensitive surname prefix matching
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
    """Return True if text looks like a judge name (starts with known title)."""
    if not text:
        return False
    text_lower = text.lower()

    # Exclude obvious non-judge entries
    exclusions = [
        "the black country", "the midlands", "the north", "the south",
        "the east", "the west", "the city", "the county", "the district",
        "the region", "the area", "the circuit", "the division"
    ]
    if any(text_lower.startswith(excl) for excl in exclusions):
        return False

    # Must start with a known judicial title
    if not any(text_lower.startswith(t.lower() + " ") for t in TITLES):
        return False

    # Additional validation: should contain at least one more word after title
    # and shouldn't be all location-like words
    for title in TITLES:
        title_lower = title.lower()
        if text_lower.startswith(title_lower + " "):
            remainder = text[len(title):].strip()
            # Must have at least one word after the title
            if not remainder or len(remainder.split()) == 0:
                return False
            # Check if remainder looks like a person's name (not all capitals for locations)
            # and contains at least 2 words for proper names
            words = remainder.split()
            if len(words) >= 1:
                # Exclude common location words
                location_words = {"country", "region", "area", "circuit", "division",
                                "midlands", "north", "south", "east", "west", "city",
                                "county", "district", "wales", "scotland", "england", "ireland"}
                if all(w.lower() in location_words for w in words):
                    return False
            return True

    return False


def scrape_page(page, url: str) -> List[Dict]:
    """Scrape all judges from one URL."""
    judges = []
    page.goto(url, wait_until="domcontentloaded", timeout=20000)

    for table in page.locator("table").all():
        for row in table.locator("tbody tr").all():
            cells = [c.inner_text().strip() for c in row.locator("td").all()]
            if not any(cells):
                continue

            full_name = cells[0]
            if not looks_like_judge(full_name):
                continue

            date_val = next((parse_date(c) for c in cells[1:] if parse_date(c)), None)
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
    """Convert None values to empty strings for DB-safe JSON."""
    for key in ["first_name", "middle_name", "last_name"]:
        if judge.get(key) is None:
            judge[key] = ''
    return judge


def main():
    """Main script for file."""
    base_url = (
        "https://www.judiciary.uk/about-the-judiciary/who-are-the-judiciary/"
        "list-of-members-of-the-judiciary/"
    )
    all_judges: List[Dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url, wait_until="domcontentloaded", timeout=20000)

        links = [a.get_attribute("href") for a in page.locator('a[href*="list-of-members"]').all()]
        links = [f"https://www.judiciary.uk{l}" if \
                 l and l.startswith("/") else l for l in links if l]

        if links:
            for link in links:
                all_judges.extend(scrape_page(page, link))
        else:
            all_judges.extend(scrape_page(page, base_url))

        browser.close()

    titles = extract_titles(all_judges)
    add_title_ids(all_judges, titles)

    # Normalise None → "" for DB-safe JSON
    normalised_judges = [normalise_judge(j) for j in all_judges]

    with open("titles_data.json", "w", encoding="utf-8") as f:
        json.dump(titles, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(titles)} unique titles -> titles_data.json")

    with open("judges_data.json", "w", encoding="utf-8") as f:
        json.dump(normalised_judges, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(normalised_judges)} judges -> judges_data.json")


if __name__ == "__main__":
    main()
