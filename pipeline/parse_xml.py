import re

from lxml import etree

# Create Regex to filter some false-positives
SUB_PATTERN = re.compile(r"^[A-Z].+")


def get_subheadings(filename: str) -> list:
    root = etree.parse(filename)

    # remove any toc if present
    toc = root.xpath(
        "//n:toc",
        namespaces={"n": "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"})
    for element in toc:
        element.getparent().remove(element)

    level_elements = []
    for element in root.iter(
            "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}level"):
        if SUB_PATTERN.match("".join(element.itertext()).strip()):
            level_elements.append(element)
    subheadings = list(filter(lambda e: "eId" in e.keys()
                       and "lvl_" in e.get("eId"), level_elements))

    for element in root.iter("{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subparagraph"):
        if SUB_PATTERN.match("".join(element.itertext())):
            level_elements.append(element)
    subheadings += list(filter(lambda e: e.find(
        "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}num") is None, level_elements))
    return subheadings


def get_text_of_subheadings(start_element, end_element) -> str:
    while start_element.getparent().tag != "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}decision":
        start_element = start_element.getparent()

    while end_element.getparent().tag != "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}decision":
        end_element = end_element.getparent()

    judgmentChildren = list(start_element.getparent())
    print(start_element.getparent())
    print(judgmentChildren)
    start_index = judgmentChildren.index(start_element)
    end_index = judgmentChildren.index(end_element)

    text = ""
    for i in range(start_index, end_index):
        print("doing stuff")
        text += "".join(judgmentChildren[i].itertext())
    return text


if __name__ == "__main__":
    unhandled_xmls = []
    all_subheadings = []
    handled_xmls = []
    for i in range(1, 1001):
        subheadings = get_subheadings(f"xmls/data_{i}.xml")
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
    # text = get_text_of_subheadings(s[0], s[1])
