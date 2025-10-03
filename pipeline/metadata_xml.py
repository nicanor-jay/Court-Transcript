"""Extract metadata from hearing transcripts."""

import argparse
import json
from datetime import datetime

from lxml import etree

# Common namespaces for XML files from https://caselaw.nationalarchives.gov.uk/
NS_MAPPING = {
    "n": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0",
    "nuk": "https://caselaw.nationalarchives.gov.uk/akn"
}


def get_case_url(meta: "etree._Element") -> str:
    """Returns case hearing URL from metadata."""
    xpath = "//n:FRBRExpression//n:FRBRthis"
    url_element = meta.xpath(xpath, namespaces=NS_MAPPING)
    if url_element:
        url_element = url_element[0]
    else:
        # return None if metadata can't be found
        return None
    return url_element.get("value")


def get_case_judgement_date(meta: "etree._Element") -> datetime:
    """Returns the date when judgement was handed down from metadata."""
    xpath = "//n:FRBRExpression//n:FRBRdate"
    date_element = meta.xpath(xpath, namespaces=NS_MAPPING)
    if date_element:
        date_element = date_element[0]
    else:
        return None
    date_str = date_element.get("date")
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_case_citation(meta: "etree._Element") -> str:
    """Returns the neutral citation, which can be used as a unique identifier."""
    xpath = "//nuk:cite"
    cite_element = meta.xpath(xpath, namespaces=NS_MAPPING)
    if cite_element:
        cite_element = cite_element[0]
    else:
        return None
    return cite_element.text


def get_case_name(meta: "etree._Element") -> str:
    """Returns the title given to the case hearing."""
    xpath = "//n:FRBRWork//n:FRBRname"
    name_element = meta.xpath(xpath, namespaces=NS_MAPPING)
    if name_element:
        name_element = name_element[0]
    else:
        return None
    return name_element.get("value")


def get_court_name(meta: "etree._Element") -> str:
    """Returns the name of the institution/court where the hearing took place."""
    xpath = "//n:TLCOrganization"
    org_element = meta.xpath(xpath, namespaces=NS_MAPPING)
    # tna (The National Archives) is also listed as an org, so we need to filter it
    org_element = list(filter(lambda e: e.get("eId") != "tna", org_element))[0]
    return org_element.get("showAs")


def get_judges(root: etree._Element) -> list[str] | None:
    """Returns a list of the judges who sat the hearing."""
    people = root.xpath("//n:TLCPerson", namespaces=NS_MAPPING)
    judges = [person.get("showAs")
              for person in people if person.get("href") != ""]
    return judges if judges else None


def get_metadata(filename: str) -> dict:
    """
    Extracts metadata from `filename` and returns it as a dictionary.
    Structure of the returned dictionary:

    `title` (`str`): The title of the hearing.
    `citation` (`str`): Neutral citation; can be used as unique identifier.
    `verdict_date` (`datetime`): The date when judgement was handed down.
    `court` (`str`): The name of the court where the hearing took place.
    `url` (`str`): A URL to the hearing transcript page.
    `judges` (`list[str]`): List of judges who sat the hearing.
    """
    if not filename.endswith(".xml"):
        raise ValueError("filename must be a .xml file")

    root = etree.parse(filename)
    try:
        meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    except IndexError as e:
        raise KeyError(f"{filename} has no meta element") from e

    metadata = {
        "title": get_case_name(meta),
        "citation": get_case_citation(meta),
        "verdict_date": get_case_judgement_date(meta),
        "court": get_court_name(meta),
        "url": get_case_url(meta)
    }

    return metadata


def output_metadata(filename: str, metadata: dict) -> None:
    """Creates JSON file `filename` and writes `metadata` to it."""
    if not filename.endswith(".json"):
        raise ValueError("filename must be a .json file")

    # datetime can't be serialized, so convert into string
    date_str = datetime.strftime(metadata["verdict_date"], "%Y-%m-%d")
    metadata["verdict_date"] = date_str

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)


def set_up_args() -> argparse.Namespace:
    """Sets up CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        type=str, required=True,
        help="XML file to process")
    parser.add_argument(
        "-o", "--output", action="store_true",
        help="If given, will output a JSON file of the same name")
    return parser.parse_args()


if __name__ == "__main__":
    args = set_up_args()
    data = get_metadata(args.file)
    if args.output:
        # change filename extension
        output_file = args.file.replace(".xml", ".json")
        # get base of path
        base_start = output_file.rfind('/')+1
        output_file = output_file[base_start:] if base_start >= 0 else output_file
        output_metadata(output_file, data)
