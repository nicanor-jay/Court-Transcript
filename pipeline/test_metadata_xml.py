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
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    name = get_case_name(meta)
    assert isinstance(name, str)


def test_get_case_name_correct_name(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    name = get_case_name(meta)
    real_name = "Fang Ankong and another v Green Elite Ltd  (Virgin Islands)"
    assert name == real_name


def test_get_case_citation_correct_type(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    citation = get_case_citation(meta)
    assert isinstance(citation, str)


def test_get_case_citation_correct_citation(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    citation = get_case_citation(meta)
    real_citation = "[2025] UKPC 47"
    assert citation == real_citation


def test_get_case_judgement_date_correct_type(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    date = get_case_judgement_date(meta)
    assert isinstance(date, datetime)


def test_get_case_judgement_date_correct_citation(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    date = get_case_judgement_date(meta)
    real_date = datetime(year=2025, month=9, day=30)
    assert date == real_date


def test_get_court_name_correct_type(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    court_name = get_court_name(meta)
    assert isinstance(court_name, str)


def test_get_court_name_correct_name(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    court_name = get_court_name(meta)
    real_court_name = "The Judicial Committee of the Privy Council"
    assert court_name == real_court_name


def test_get_case_url_correct_type(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    url = get_case_url(meta)
    assert isinstance(url, str)


def test_get_case_url_correct_name(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    url = get_case_url(meta)
    real_url = "https://caselaw.nationalarchives.gov.uk/ukpc/2025/47"
    assert url == real_url


def test_get_judges_correct_type(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    judges = get_judges(meta)
    assert isinstance(judges, list)


def test_get_judges_correct_elements_type(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    judges = get_judges(meta)
    assert all(isinstance(judge, str) for judge in judges)


def test_get_judges_correct_name(xml_metadata):
    root = etree.fromstring(xml_metadata)
    meta = root.xpath("//n:meta", namespaces=NS_MAPPING)[0]
    judges = get_judges(meta)
    real_judges = ['Lord Briggs', 'Lord Sales',
                   'Lord Hamblen', 'Lord Burrows', 'Lord Richards']
    assert judges == real_judges


def test_get_metadata_rejects_bad_filename():
    with pytest.raises(ValueError) as exc_info:
        get_metadata("bad_file.csv")
        assert "filename must be a .xml file" in exc_info.value


def test_get_metadata_returns_dict(xml_metadata):
    etree.parse = Mock(return_value=etree.fromstring(xml_metadata))
    metadata = get_metadata("dummy.xml")
    assert isinstance(metadata, dict)


def test_get_metadata_dict_has_correct_keys(xml_metadata):
    etree.parse = Mock(return_value=etree.fromstring(xml_metadata))
    metadata = get_metadata("dummy.xml")
    assert list(metadata.keys()) == ['title', 'citation',
                                     'verdict_date', 'court', 'url']
