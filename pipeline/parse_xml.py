import re

from lxml import etree

# Create Regex to filter some false-positives
SUB_PATTERN = re.compile(r"^[A-Z].+")
# Common namespace for XML files from https://caselaw.nationalarchives.gov.uk/
NAMESPACE = "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}"


def get_headings_level_approach(root: "etree._ElementTree") -> list["etree._Element"]:
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


def get_headings_subparagraph_approach(root: "etree._ElementTree") -> list["etree._Element"]:
    """
    Finds headings in `root` by finding <subparagraph> tags which
    do not contain any <num> elements as children. All elements in
    `root` which match this criteria are assumed to be headings.
    """
    matched_elements = []
    for element in root.iter(NAMESPACE + "subparagraph"):
        if SUB_PATTERN.match("".join(element.itertext())):
            matched_elements.append(element)

    return list(filter(lambda e: e.find(NAMESPACE + "num") is None, matched_elements))


def get_headings(filename: str) -> list["etree._Element"]:
    """
    This function - through several methods - will attempt to extract
    headings from `filename` and return them as a list of their parent
    elements.
    """
    root = etree.parse(filename)

    # We need to remove any <toc> (Table of Contents) tags since
    # this will lead to duplicates and may mess with text extraction
    toc_elements = root.xpath("//n:toc", namespaces={"n": NAMESPACE})
    for toc in toc_elements:
        toc.getparent().remove(toc)

    headings = get_headings_level_approach(root)
    headings += get_headings_subparagraph_approach(root)

    return headings


def get_text_between_elements(start_element, end_element) -> str:
    """
    Collects all raw text between `start_element` and `end_element`
    in an XML document.
    """

    # decision is the tag which contains all of the judgement data
    # i.e. it is an ancestor of all the tags we care about
    decision_tag_str = NAMESPACE + "decision"

    # we find the ancestor of the start and end element
    # whose immediate parent is the decision element
    while start_element.getparent().tag != decision_tag_str:
        start_element = start_element.getparent()
    while end_element.getparent().tag != decision_tag_str:
        end_element = end_element.getparent()

    # we're using start_element.getparent() as a shortcut
    # to the <decision> tag, which parents all tags
    all_tags = list(start_element.getparent())

    # find the index of start, and where we should go up to
    start_index = all_tags.index(start_element)
    end_index = all_tags.index(end_element)

    text = ""
    # collect all of the text in the elements
    # between start and end indexes
    for i in range(start_index, end_index):
        text += "".join(all_tags[i].itertext())
    return text


if __name__ == "__main__":
    unhandled_xmls = []
    all_subheadings = []
    handled_xmls = []
    for i in range(1, 1001):
        subheadings = get_headings(f"xmls/data_{i}.xml")
        if len(subheadings) == 0:
            print(f"xmls/data_{i}.xml not parsed")
            unhandled_xmls.append(f"xmls/data_{i}.xml")
        else:
            all_subheadings.append(subheadings)
            handled_xmls.append(f"xmls/data_{i}.xml")
    percentage_handled = (1000 - len(unhandled_xmls)) / 1000 * 100
    print("\n============================\n")
    subheadings_counts = [len(subheadings) for subheadings in all_subheadings]
    avg_no_subheadings = sum(subheadings_counts) / len(all_subheadings)
    print(f"Total files correctly parsed: {percentage_handled:.2f}")
    print(f"Average No. subheadings per transcript: {avg_no_subheadings}")
    # print(sorted(subheadings_counts, reverse=True))
    # print(subheadings_counts.index(3))
    # with open("temp.txt", "w", encoding="utf-8") as f:
    #     for element in all_subheadings[14]:
    #         line = "".join(element.itertext()) + "\n"
    #         f.write(line)
    s = all_subheadings[0]
    # text = get_text_between_elements(s[0], s[1])
