# pylint: skip-file

"""Tests for parse_xml.py heading detection"""

from unittest.mock import Mock

from lxml import etree

from parse_xml import (
    get_headings
)


def test_get_headings_natural_xml_correct_length(xml_natural_file):
    # etree.parse = Mock(return_value=etree.fromstring(xml_natural_file))
    root = etree.fromstring(xml_natural_file)
    headings = get_headings(root)
    assert len(headings) == 2


def test_get_headings_natural_xml_correct_elements(xml_natural_file):
    root = etree.fromstring(xml_natural_file)
    headings = get_headings(root)
    text = ""
    for element in headings:
        text += "".join(element.itertext())
    # We need to check that the text is from headings only
    assert "The facts" in text
    assert "The legal framework:" in text
    assert "And if there has been an unjustified" not in text
    assert "Whether the payments by Mr" not in text
