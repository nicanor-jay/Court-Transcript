"""National Archive XML Fetcher. """
# pylint:disable=logging-fstring-interpolation
import xml.etree.ElementTree as ET
from pathlib import Path
import re
from typing import List, Tuple, Optional, Dict
import argparse
import logging
import requests

BASE_FEED_URL = "https://caselaw.nationalarchives.gov.uk/atom.xml"
NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
    "tna": "https://caselaw.nationalarchives.gov.uk"
}

out_dir = Path("/tmp/xml_cases")
out_dir.mkdir(exist_ok=True)


def setup_logging() -> None:
    """Configure logging output."""
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging initialised.")


def slugify(text: str) -> str:
    """
    Make a safe filename from a string (max length 100 chars).

    Example:
        "Smith v. Jones [2024] UKSC 123" -> "Smith_v__Jones__2024__UKSC_123"
        "R (on the application of Miller)" -> "R__on_the_application_of_Miller_"
    """
    return re.sub(r'[^a-zA-Z0-9_-]+', '_', text)[:100]


def fetch_feed(per_page: int = 20) -> ET.Element:
    """Fetch the Atom feed with the specified batch size."""
    url = f"{BASE_FEED_URL}?per_page={per_page}"
    r = requests.get(url, timeout=1000)
    r.raise_for_status()
    return ET.fromstring(r.content)


def get_xml_entries(feed: ET.Element) -> List[Tuple[str, str, Optional[str]]]:
    """
    Extract entries from the Atom feed.
    Returns a list of (title, uri, href-to-xml-or-None).
    """
    entries = []
    for entry in feed.findall("atom:entry", NAMESPACES):
        title = entry.find("atom:title", NAMESPACES).text
        uri = entry.find("tna:uri", NAMESPACES).text
        xml_link = entry.find(
            'atom:link[@type="application/akn+xml"]', NAMESPACES)
        href = xml_link.attrib["href"] if xml_link is not None else None
        entries.append((title, uri, href))
    return entries


def load_single_xml(entry: Tuple[str, str, Optional[str]], xml_dict: Dict[str, str]) -> None:
    """
    Fetch XML for a single entry and store in xml_dict.
    Key = slugified title, Value = raw XML string.
    """
    title, uri, href = entry
    if href:
        try:
            resp = requests.get(href, timeout=1000)
            resp.raise_for_status()
            xml_dict[slugify(title)] = resp.text
        except (requests.exceptions.RequestException, TimeoutError) as e:
            logging.error(f"Failed to load {title} ({href}): {e}")
    else:
        logging.warning(f"No XML for: {title} ({uri})")


def load_all_xml(entries: List[Tuple[str, str, Optional[str]]]) -> Dict[str, str]:
    """Load XMLs for all entries into a dictionary."""
    xml_dict = {}
    for entry in entries:
        load_single_xml(entry, xml_dict)
    return xml_dict


def download_from_dict(xml_dict: Dict[str, str]) -> None:
    """Write XMLs from xml_dict to disk."""
    for slug, xml_str in xml_dict.items():
        filepath = out_dir / f"{slug}.xml"
        try:
            filepath.write_text(xml_str, encoding="utf-8")
            logging.info(f"Saved: {filepath}")
        except OSError as e:  # catch all file write errors
            logging.error(f"Failed to save {slug}: {e}")


def main():
    """Main Function; handles argparse. """
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Fetch National Archives court XMLs.")
    parser.add_argument("--per-page", type=int,
                        default=10, help="Number of cases to fetch (default 10).")
    parser.add_argument("--download", action="store_true",
                        help="Save XMLs to disk as files.")
    args = parser.parse_args()

    feed = fetch_feed(per_page=args.per_page)
    entries = get_xml_entries(feed)

    xml_strings = load_all_xml(entries)  # always in memory
    logging.info(f"Loaded {len(xml_strings)} XMLs into memory")

    if args.download:
        download_from_dict(xml_strings)


if __name__ == "__main__":
    main()
