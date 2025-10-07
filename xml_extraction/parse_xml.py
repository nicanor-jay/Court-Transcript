"""Module which roughly extracts heading sections out of hearing transcripts."""

import re

from lxml import etree

# Some of the rules we have set up will still let
# false-positives through; many of these are
# mid-sentence fragments, or the start of a
# paragraph (which is almost always preceded
# by a number). See below for examples.
#
# A mid-sentence fragment may look like:
# and the respondent claims that this was in error...
#
# Another common false-positive is with quotations:
# "does not believe that [the act] was done in good faith."
#
# And, very often, the opening of a paragraph (preceded with a number):
# 14 The existing regulations show that...
#
# The regex pattern below simply enforces that a heading must be
# started with a capital letter. The justification for this is really
# just that this is what we have seen to be true for most, if not
# all headings. It is also a simple enough rule that it will not
# 'over-correct' and create a lot of false-negatives.
SUB_PATTERN = re.compile(r"^[A-Z].+")
# Common namespace for XML files from https://caselaw.nationalarchives.gov.uk/
NAMESPACE = "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}"


def find_headings_level_rule(root: "etree._ElementTree") -> list["etree._Element"]:
    """
    Finds headings in `root` by finding <level> tags which have an
    attribute that matches `lvl_XX`. All elements in `root` which
    match this criteria are assumed to contain headings.
    """
    def ensure_lvl_attr(e):
        # This is a filter function to ensure `e` has an
        # `eId` attribute and that its value contains `lvl_`
        return "eId" in e.keys() and "lvl_" in e.get("eId")

    matched_elements = []
    # look through every <level> element
    for element in root.iter(NAMESPACE + "level"):
        if SUB_PATTERN.match("".join(element.itertext()).strip()):
            # element text matches filter regex
            matched_elements.append(element)

    return list(filter(ensure_lvl_attr, matched_elements))


def find_headings_subparagraph_rule(root: "etree._ElementTree") -> list["etree._Element"]:
    """
    Finds headings in `root` by finding <subparagraph> tags which
    do not contain any <num> elements as children. All elements in
    `root` which match this criteria are assumed to be headings.
    """
    matched_elements = []
    for element in root.iter(NAMESPACE + "subparagraph"):
        if SUB_PATTERN.match("".join(element.itertext()).strip()):
            matched_elements.append(element)

    return list(filter(lambda e: e.find(NAMESPACE + "num") is None, matched_elements))


def get_headings(root: "etree._ElementTree") -> list["etree._Element"] | None:
    """
    This function - through several methods - will attempt to extract
    headings from `filename` and return them as a list of their parent
    elements.
    """

    # We need to remove any <toc> (Table of Contents) tags since
    # this will lead to duplicates and may mess with text extraction
    # NAMESPACE[1:-1] is used to remove the {} brackets
    toc_elements = root.xpath(
        "//n:toc",
        namespaces={"n": NAMESPACE.strip("{}")}
    )
    for toc in toc_elements:
        toc.getparent().remove(toc)

    headings = find_headings_level_rule(root)
    headings += find_headings_subparagraph_rule(root)

    # headings may be out of order with respect to the original XML doc
    # first grab the parent of the judgement text
    decision_element = list(root.iter(NAMESPACE + "decision"))[0]
    # then its children elements
    all_tags = list(decision_element.iter())
    # sort heading elements according to their occurrence in all_tags
    try:
        headings.sort(key=all_tags.index)
    except ValueError:
        return None

    return headings


def get_text_between_elements(
    root: etree._ElementTree,
    start_element: etree._Element = None,
    end_element: etree._Element = None
) -> str:
    """
    Collects all raw text between `start_element` and `end_element`
    in an XML document.

    If `start_element` is None, then begin from start of judgement body.
    Similarly, if `end_element` is None, read until end of judgement body.

    It is an error for both `start_element` and `end_element` to be None.
    """
    if start_element is None and end_element is None:
        raise TypeError("start_element and end_element cannot both be None")

    # decision is the tag which contains all of the judgement data
    # i.e. it is an ancestor of all the tags we care about
    decision_tag_str = NAMESPACE + "decision"
    # find the <decision> element itself
    # and then its children
    decision_element = list(root.iter(decision_tag_str))[0]
    all_tags = list(decision_element)

    # we find the ancestor of the start and end element
    # whose immediate parent is the decision element
    # if either one is None, then we substitute with
    # the first or last element in decision accordingly
    if start_element is not None:
        while start_element.getparent().tag != decision_tag_str:
            start_element = start_element.getparent()
        start_index = all_tags.index(start_element)
    else:
        start_index = 0

    if end_element is not None:
        while end_element.getparent().tag != decision_tag_str:
            end_element = end_element.getparent()
        end_index = all_tags.index(end_element)
    else:
        end_index = len(all_tags)-1

    text = ""
    # collect all of the text in the elements
    # between start and end indexes
    for i in range(start_index, end_index):
        text += "".join(all_tags[i].itertext())
    return text


def get_label_text_dict(xml_string: str) -> dict[str, str] | None:
    """
    Returns a dictionary containing {label: key} pairs
    corresponding to a heading in `xml_string` and the
    raw text in that section. `xml_string` must be an XML str.
    """

    if not isinstance(xml_string, str):
        raise ValueError("filename must be a str")

    root = etree.fromstring(xml_string.encode())
    headings = get_headings(root)

    if not headings:
        return None

    text_pairings = {}
    # Get text up to first heading
    # labeled as 'DOC_START'
    raw_text = get_text_between_elements(root, end_element=headings[0])
    if raw_text != "":
        text_pairings["DOC_START"] = raw_text

    for i, heading in enumerate(headings):
        if i >= len(headings)-1:
            # skip the last element as there is
            # no next heading to read up to
            continue
        header_text = "".join(heading.itertext()).strip()
        raw_text = get_text_between_elements(root, headings[0], headings[1])
        text_pairings[header_text] = raw_text

    # Get from last heading til end
    # labeled as 'DOC_END'
    raw_text = get_text_between_elements(root, start_element=headings[-1])
    if raw_text != "":
        text_pairings["DOC_END"] = raw_text

    return text_pairings
