"""Extract metadata from hearing transcripts."""

from lxml import etree

# Common namespace for XML files from https://caselaw.nationalarchives.gov.uk/
NAMESPACE = "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}"

if __name__ == "__main__":
    root = etree.parse("xmls/data_1.xml")
    meta = list(root.iter(NAMESPACE + "meta"))[0]
