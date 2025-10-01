"""Extract metadata from hearing transcripts."""

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


def get_case_judgement_data(meta: "etree._Element") -> str:
    """Returns the date when judgement was handed down from metadata."""
    xpath = "//n:FRBRExpression//n:FRBRdate"
    date_element = meta.xpath(xpath, namespaces=NS_MAPPING)[0]
    return date_element.get("date")


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


if __name__ == "__main__":
    root = etree.parse("xmls/data_1.xml")
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    url = get_case_url(meta)
    date = get_case_judgement_data(meta)
    cite = get_case_citation(meta)
    name = get_case_name(meta)
    court_name = get_court_name(meta)
