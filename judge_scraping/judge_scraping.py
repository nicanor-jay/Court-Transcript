"""
UK Judiciary Web Scraper - Judges Only
Scrapes judiciary.uk and extracts *only* real judges.
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright

# Judicial titles (longest first to avoid partial matches)
TITLES = [
    "District Judge (MC)", "District Judge",
    "Lord Justice", "Lady Justice",
    "His Honour Judge", "Her Honour Judge",
    "His Honour", "Her Honour",
    "Lord", "Lady", "Sir", "Dame",
    "Mr", "Mrs", "Miss", "Ms",
    "Dr", "Professor",
    "Judge", "HHJ", "DHJ",
]

# Post-nominal titles to strip from the end
POST_NOMINALS = ["KC", "QC", "CBE", "OBE", "MBE", "JP"]

# Prefixes that indicate multi-word surnames
SURNAME_PREFIXES = ["van", "van der", "van den", "de", "de la", "du", "von", "von der"]


def parse_date(text: str) -> Optional[str]:
    """Parse a date string into ISO format if possible."""
    if not text:
        return None
    text = text.strip()
    formats = [
        "%d %B %Y", "%d %b %Y",
        "%d/%m/%Y", "%d-%m-%Y",
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

    # Extract title
    for title in TITLES:
        if full.startswith(title + " "):
            result["title"] = title
            full = full[len(title):].strip()
            break

    # Strip post-nominals from the end
    for post_nom in POST_NOMINALS:
        if full.endswith(" " + post_nom):
            full = full[:-len(post_nom)].strip()

    parts = full.split()
    if not parts:
        return result
    
    if len(parts) == 1:
        result["last_name"] = parts[0]
        return result
    
    # Check for surname prefixes (longest match first)
    surname_start_idx = None
    for prefix in sorted(SURNAME_PREFIXES, key=len, reverse=True):
        prefix_parts = prefix.split()
        for i in range(len(parts) - len(prefix_parts)):
            if " ".join(parts[i:i+len(prefix_parts)]).lower() == prefix:
                surname_start_idx = i
                break
        if surname_start_idx is not None:
            break
    
    if surname_start_idx is not None:
        # We found a prefix - everything from there is the surname
        if surname_start_idx == 0:
            # Surname prefix is at the start, no first name
            result["last_name"] = " ".join(parts[surname_start_idx:])
        else:
            result["first_name"] = parts[0]
            if surname_start_idx > 1:
                result["middle_name"] = " ".join(parts[1:surname_start_idx])
            result["last_name"] = " ".join(parts[surname_start_idx:])
    else:
        # No prefix found - standard parsing
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
    return any(text.startswith(t + " ") for t in TITLES)


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
                continue  # skip nonjudge entries

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
    seen_titles = set()
    titles = []
    
    for judge in judges:
        title_name = judge.get("title")
        if title_name and title_name not in seen_titles:
            seen_titles.add(title_name)
            titles.append({
                "title_id": len(titles) + 1,
                "title_name": title_name
            })
    
    # Sort alphabetically for consistency
    titles.sort(key=lambda x: x["title_name"])
    
    # Reassign IDs after sorting
    for idx, title in enumerate(titles, start=1):
        title["title_id"] = idx
    
    return titles


def add_title_ids(judges: List[Dict], titles: List[Dict]) -> None:
    """Add title_id to each judge based on the titles lookup."""
    title_map = {t["title_name"]: t["title_id"] for t in titles}
    
    for judge in judges:
        title_name = judge.get("title")
        judge["title_id"] = title_map.get(title_name) if title_name else None


def main():
    base_url = "https://www.judiciary.uk/about-the-judiciary/who-are-the-judiciary/list-of-members-of-the-judiciary/"
    all_judges: List[Dict] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(base_url, wait_until="domcontentloaded", timeout=20000)

        # Collect sublinks
        links = [a.get_attribute("href") for a in page.locator('a[href*="list-of-members"]').all()]
        links = [f"https://www.judiciary.uk{l}" if l and l.startswith("/") else l for l in links if l]

        if links:
            for link in links:
                all_judges.extend(scrape_page(page, link))
        else:
            all_judges.extend(scrape_page(page, base_url))

        browser.close()

    # Extract and normalize titles
    titles = extract_titles(all_judges)
    add_title_ids(all_judges, titles)

    # Save titles
    with open("titles_data.json", "w", encoding="utf-8") as f:
        json.dump(titles, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(titles)} unique titles -> titles_data.json")

    # Save judges
    with open("judges_data.json", "w", encoding="utf-8") as f:
        json.dump(all_judges, f, indent=2, ensure_ascii=False)
    print(f"Extracted {len(all_judges)} judges -> judges_data.json")


if __name__ == "__main__":
    main()