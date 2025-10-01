# pylint: skip-file

"""Tests for parse_xml.py heading detection"""

from unittest.mock import Mock

from lxml import etree

from parse_xml import (
    get_headings,
    get_headings_level_approach,
    get_headings_subparagraph_approach,
    get_text_between_elements
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


def test_get_headings_no_headings_correct_length(xml_no_headings):
    root = etree.fromstring(xml_no_headings)
    headings = get_headings(root)
    assert len(headings) == 0


def test_get_headings_reverse_headings_correct_order(xml_reverse_order):
    root = etree.fromstring(xml_reverse_order)
    headings = get_headings(root)
    assert len(headings) == 2
    assert headings[0].tag == "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}subparagraph"
    assert headings[1].tag == "{http://docs.oasis-open.org/legaldocml/ns/akn/3.0}level"


def test_get_headings_level_approach_headings_only_correct_length(xml_all_headings):
    root = etree.fromstring(xml_all_headings)
    headings = get_headings_level_approach(root)
    assert len(headings) == 2


def test_get_headings_level_approach_headings_only_correct_elements(xml_all_headings):
    root = etree.fromstring(xml_all_headings)
    headings = get_headings_level_approach(root)
    text = ""
    for element in headings:
        text += "".join(element.itertext())
    # ensure that sub style headings weren't grabbed
    assert "The facts" in text
    assert "The legal framework:" not in text


def test_get_headings_subparagraph_approach_headings_only_correct_length(xml_all_headings):
    root = etree.fromstring(xml_all_headings)
    headings = get_headings_subparagraph_approach(root)
    assert len(headings) == 2


def test_get_headings_subparagraph_approach_headings_only_correct_elements(xml_all_headings):
    root = etree.fromstring(xml_all_headings)
    headings = get_headings_subparagraph_approach(root)
    text = ""
    for element in headings:
        text += "".join(element.itertext())
    # ensure that level style headings weren't grabbed
    assert "The facts" not in text
    assert "The legal framework:" in text


def test_get_text_between_elements_correct_text(xml_natural_file):
    # only two headings in natural file
    # with one LEVEL_NON_HEADING between them
    root = etree.fromstring(xml_natural_file)
    headings = get_headings(root)
    text = get_text_between_elements(root, headings[0], headings[1])
    # ensure only level non heading is in text
    assert "And if there has been an unjustified" in text
    assert "Whether the payments by Mr" not in text
