# pylint: skip-file

from unittest.mock import Mock
from datetime import datetime

import pytest
from lxml import etree

from metadata_xml import (
    NS_MAPPING,
    get_case_name,
    get_case_citation,
    get_case_judgement_date,
    get_court_name,
    get_case_url,
    get_judges,
    get_metadata
)


def test_get_case_name_correct_type(xml_metadata):
    """Check case name is a string."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    name = get_case_name(meta)
    assert isinstance(name, str)


def test_get_case_name_correct_name(xml_metadata):
    """Check case name is correct."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    name = get_case_name(meta)
    real_name = "Fang Ankong and another v Green Elite Ltd  (Virgin Islands)"
    assert name == real_name


def test_get_case_citation_correct_type(xml_metadata):
    """Check citation is a string."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    citation = get_case_citation(meta)
    assert isinstance(citation, str)


def test_get_case_citation_correct_citation(xml_metadata):
    """Check citation is correct."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    citation = get_case_citation(meta)
    real_citation = "[2025] UKPC 47"
    assert citation == real_citation


def test_get_case_judgement_date_correct_type(xml_metadata):
    """Check judgement date is datetime."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    date = get_case_judgement_date(meta)
    assert isinstance(date, datetime)


def test_get_case_judgement_date_correct_citation(xml_metadata):
    """Check judgement date is correct."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    date = get_case_judgement_date(meta)
    real_date = datetime(year=2025, month=9, day=30)
    assert date == real_date


def test_get_court_name_correct_type(xml_metadata):
    """Test court name is string."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    court_name = get_court_name(meta)
    assert isinstance(court_name, str)


def test_get_court_name_correct_name(xml_metadata):
    """Test court name is correct."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    court_name = get_court_name(meta)
    real_court_name = "The Judicial Committee of the Privy Council"
    assert court_name == real_court_name


def test_get_case_url_correct_type(xml_metadata):
    """Test url is string."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    url = get_case_url(meta)
    assert isinstance(url, str)


def test_get_case_url_is_correct(xml_metadata):
    """Test url is correct."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    url = get_case_url(meta)
    real_url = "https://caselaw.nationalarchives.gov.uk/ukpc/2025/47"
    assert url == real_url


def test_get_judges_correct_type(xml_metadata):
    """Test judges is a list."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    judges = get_judges(meta)
    assert isinstance(judges, list)


def test_get_judges_correct_elements_type(xml_metadata):
    """Test judges elements are all strings."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    judges = get_judges(meta)
    assert all(isinstance(judge, str) for judge in judges)


def test_get_judges_correct_name(xml_metadata):
    """Test names in judges is correct."""
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    judges = get_judges(meta)
    real_judges = ['Lord Briggs', 'Lord Sales',
                   'Lord Hamblen', 'Lord Burrows', 'Lord Richards']
    assert judges == real_judges


def test_get_metadata_rejects_bad_xml_string_type():
    """Test get metadata rejects bad xml_string."""
    with pytest.raises(TypeError) as exc_info:
        get_metadata(101)
        assert "xml_string must be a str type" in exc_info.value


def test_get_metadata_returns_dict(xml_metadata):
    """Test get metadata returns a dictionary."""
    metadata = get_metadata(xml_metadata.decode("utf-8"))
    assert isinstance(metadata, dict)


def test_get_metadata_dict_has_correct_keys(xml_metadata):
    """Test get metadata dictionary has correct keys."""
    metadata = get_metadata(xml_metadata.decode("utf-8"))
    assert list(metadata.keys()) == ['title', 'citation', 'verdict_date',
                                     'court', 'url', 'judges']
