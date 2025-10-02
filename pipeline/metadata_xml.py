"""Extract metadata from hearing transcripts."""

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
    url_element = meta.xpath(xpath, namespaces=NS_MAPPING)[0]
    return url_element.get("value")


def get_case_judgement_date(meta: "etree._Element") -> datetime:
    """Returns the date when judgement was handed down from metadata."""
    xpath = "//n:FRBRExpression//n:FRBRdate"
    date_element = meta.xpath(xpath, namespaces=NS_MAPPING)[0]
    date_str = date_element.get("date")
    return datetime.strptime(date_str, "%Y-%m-%d")


def get_case_citation(meta: "etree._Element") -> str:
    """Returns the neutral citation, which can be used as a unique identifier."""
    xpath = "//nuk:cite"
    cite_element = meta.xpath(xpath, namespaces=NS_MAPPING)[0]
    return cite_element.text


def get_case_name(meta: "etree._Element") -> str:
    """Returns the title given to the case hearing."""
    xpath = "//n:FRBRWork//n:FRBRname"
    name_element = meta.xpath(xpath, namespaces=NS_MAPPING)[0]
    return name_element.get("value")


def get_court_name(meta: "etree._Element") -> str:
    """Returns the name of the institution/court where the hearing took place."""
    xpath = "//n:TLCOrganization"
    org_element = meta.xpath(xpath, namespaces=NS_MAPPING)
    # tnc (The National Archives) is also listed as an org, so we need to filter it
    org_element = list(filter(lambda e: e.get("eId") != "tna", org_element))[0]
    return org_element.get("showAs")


def get_metadata(filename: str) -> dict:
    """
    Extracts metadata from `filename` and returns it as a dictionary.
    Structure of the returned dictionary:

    `title` (`str`): The title of the hearing.
    `citation` (`str`): Neutral citation; can be used as unique identifier.
    `verdict_date` (`datetime`): The date when judgement was handed down.
    `court` (`str`): The name of the court where the hearing took place.
    `url` (`str`): A URL to the hearing transcript page.
    """
    if not filename.endswith(".xml"):
        raise ValueError("filename must be a .xml file")

    root = etree.parse(filename)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]

    metadata = {
        "title": get_case_name(meta),
        "citation": get_case_citation(meta),
        "verdict_date": get_case_judgement_date(meta),
        "court": get_court_name(meta),
        "url": get_case_url(meta)
    }

    return metadata


if __name__ == "__main__":
    data = get_metadata("xmls/data_1.xml")
