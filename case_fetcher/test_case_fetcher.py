"""
Unit tests for the `case_fetcher` module.

This module tests the core functionalities of `case_fetcher`, including:
- Slugifying case titles
- Fetching Atom feeds from the UK National Archives
- Extracting XML links from feed entries
- Loading single and multiple XML files
- Downloading XML content to local files
- The main workflow integration

Uses pytest and responses for mocking HTTP requests.
"""
#pylint:disable=too-many-arguments, too-many-positional-arguments
import xml.etree.ElementTree as ET
from pathlib import Path
from unittest.mock import patch
import logging
import pytest
import responses
import case_fetcher


class TestSlugify:
    """Tests for the `slugify` function in `case_fetcher`."""

    def test_slugify_basic(self):
        """Ensure basic text is converted with underscores."""
        result = case_fetcher.slugify("Simple Text")
        assert result == "Simple_Text"

    def test_slugify_special_chars(self):
        """Ensure special characters are removed or replaced."""
        result = case_fetcher.slugify("Case [2024] UKSC/1")
        assert result == "Case_2024_UKSC_1"

    def test_slugify_long_text(self):
        """Ensure slug is truncated to maximum length (100)."""
        long_text = "A" * 150
        result = case_fetcher.slugify(long_text)
        assert len(result) == 100

    def test_slugify_multiple_special_chars(self):
        """Ensure multiple special characters are correctly handled."""
        result = case_fetcher.slugify("Test!!!Case???[2024]")
        assert result == "Test_Case_2024_"

    def test_slugify_preserves_hyphens_underscores(self):
        """Ensure hyphens and underscores are preserved in slugs."""
        result = case_fetcher.slugify("Test-Case_Name")
        assert result == "Test-Case_Name"


class TestFetchFeed:
    """Tests for the `fetch_feed` function."""

    @responses.activate
    def test_fetch_feed_success(self, sample_feed):
        """Test successful retrieval of Atom feed."""
        responses.add(
            responses.GET,
            f"{case_fetcher.BASE_FEED_URL}?per_page=10",
            body=sample_feed,
            status=200
        )

        feed = case_fetcher.fetch_feed(per_page=10)
        assert feed is not None
        assert feed.tag.endswith("feed")

    @responses.activate
    def test_fetch_feed_custom_per_page(self, sample_feed):
        """Test fetching feed with a custom `per_page` parameter."""
        responses.add(
            responses.GET,
            f"{case_fetcher.BASE_FEED_URL}?per_page=25",
            body=sample_feed,
            status=200
        )

        feed = case_fetcher.fetch_feed(per_page=25)
        assert feed is not None

    @responses.activate
    def test_fetch_feed_http_error(self):
        """Test feed fetching when server returns an HTTP error."""
        responses.add(
            responses.GET,
            f"{case_fetcher.BASE_FEED_URL}?per_page=10",
            status=404
        )

        with pytest.raises(Exception):
            case_fetcher.fetch_feed(per_page=10)


class TestGetXmlEntries:
    """Tests for the `get_xml_entries` function."""

    def test_get_xml_entries_all_fields(self, sample_feed):
        """Ensure all expected fields are extracted from feed entries."""
        feed = ET.fromstring(sample_feed)
        entries = case_fetcher.get_xml_entries(feed)

        assert len(entries) == 3
        assert entries[0][0] == "Sample Case v Another Case [2024] UKSC 1"
        assert entries[0][1] == "https://caselaw.nationalarchives.gov.uk/id/uksc/2024/1"
        assert entries[0][2] == "https://example.com/case1.xml"

    def test_get_xml_entries_missing_xml_link(self, sample_feed):
        """Ensure entries without XML links return `None` for href."""
        feed = ET.fromstring(sample_feed)
        entries = case_fetcher.get_xml_entries(feed)

        assert entries[2][2] is None

    def test_get_xml_entries_empty_feed(self):
        """Ensure empty feeds return an empty list."""
        empty_feed = """<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom" xmlns:tna="https://caselaw.nationalarchives.gov.uk">
        </feed>
        """
        feed = ET.fromstring(empty_feed)
        entries = case_fetcher.get_xml_entries(feed)

        assert len(entries) == 0


class TestLoadSingleXml:
    """Tests for the `load_single_xml` function."""

    @responses.activate
    def test_load_single_xml_success(self, sample_xml):
        """Ensure a single XML file is correctly loaded into a dictionary."""
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            body=sample_xml,
            status=200
        )

        entry = ("Sample Case", "uri", "https://example.com/case1.xml")
        xml_dict = {}

        case_fetcher.load_single_xml(entry, xml_dict)

        assert "Sample_Case" in xml_dict
        assert xml_dict["Sample_Case"] == sample_xml

    @responses.activate
    def test_load_single_xml_http_error(self, caplog):
        """Ensure HTTP errors are handled gracefully and logged."""
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            status=500
        )

        entry = ("Sample Case", "uri", "https://example.com/case1.xml")
        xml_dict = {}

        case_fetcher.load_single_xml(entry, xml_dict)

        assert "Failed to load" in caplog.text
        assert "Sample_Case" not in xml_dict

    def test_load_single_xml_no_href(self, caplog):
        """Ensure entries with no XML link are logged and skipped."""
        entry = ("Sample Case", "uri", None)
        xml_dict = {}

        case_fetcher.load_single_xml(entry, xml_dict)

        assert "No XML for" in caplog.text
        assert len(xml_dict) == 0


class TestLoadAllXml:
    """Tests for the `load_all_xml` function."""

    @responses.activate
    def test_load_all_xml_multiple_entries(self, sample_xml):
        """Ensure multiple XML files are loaded correctly."""
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            body=sample_xml,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case2.xml",
            body=sample_xml,
            status=200
        )

        entries = [
            ("Case One", "uri1", "https://example.com/case1.xml"),
            ("Case Two", "uri2", "https://example.com/case2.xml")
        ]

        xml_dict = case_fetcher.load_all_xml(entries)

        assert len(xml_dict) == 2
        assert "Case_One" in xml_dict
        assert "Case_Two" in xml_dict

    @responses.activate
    def test_load_all_xml_mixed_success_failure(self, sample_xml):
        """Ensure failed XML loads are skipped, successful ones stored."""
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            body=sample_xml,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case2.xml",
            status=404
        )

        entries = [
            ("Case One", "uri1", "https://example.com/case1.xml"),
            ("Case Two", "uri2", "https://example.com/case2.xml")
        ]

        xml_dict = case_fetcher.load_all_xml(entries)

        assert len(xml_dict) == 1
        assert "Case_One" in xml_dict


class TestDownloadFromDict:
    """Tests for the `download_from_dict` function."""

    def test_download_from_dict_success(self, tmp_path, monkeypatch, sample_xml):
        """Ensure XML dictionary is correctly saved to disk."""
        monkeypatch.setattr(case_fetcher, "out_dir", tmp_path)

        xml_dict = {
            "test_case": sample_xml,
            "another_case": sample_xml
        }

        case_fetcher.download_from_dict(xml_dict)

        assert (tmp_path / "test_case.xml").exists()
        assert (tmp_path / "another_case.xml").exists()
        assert (tmp_path / "test_case.xml").read_text() == sample_xml

    def test_download_from_dict_write_error(self, tmp_path, monkeypatch, caplog, sample_xml):
        """Ensure write errors are logged but do not crash execution."""
        monkeypatch.setattr(case_fetcher, "out_dir", tmp_path)

        xml_dict = {"test_case": sample_xml}

        with patch.object(Path, 'write_text', side_effect=IOError("Write error")):
            case_fetcher.download_from_dict(xml_dict)

        assert "Failed to save" in caplog.text

    def test_download_from_dict_empty_dict(self, tmp_path, monkeypatch):
        """Ensure empty dictionary results in no files written."""
        monkeypatch.setattr(case_fetcher, "out_dir", tmp_path)

        xml_dict = {}
        case_fetcher.download_from_dict(xml_dict)

        assert len(list(tmp_path.iterdir())) == 0


class TestMain:
    """Integration tests for the `main` function."""

    @responses.activate
    def test_main_default_args(self, monkeypatch, tmp_path, caplog, sample_feed, sample_xml):
        """Test main workflow with default arguments (no download)."""
        monkeypatch.setattr(case_fetcher, "out_dir", tmp_path)
        monkeypatch.setattr('sys.argv', ['case_fetcher.py'])

        responses.add(
            responses.GET,
            f"{case_fetcher.BASE_FEED_URL}?per_page=10",
            body=sample_feed,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            body=sample_xml,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case2.xml",
            body=sample_xml,
            status=200
        )

        with caplog.at_level(logging.INFO):
            case_fetcher.main()

        assert "Loaded" in caplog.text
        assert "2 XMLs" in caplog.text
        assert not (tmp_path / "Sample_Case_v_Another_Case__2024__UKSC_1.xml").exists()

    @responses.activate
    def test_main_with_download_flag(self, monkeypatch, tmp_path, sample_feed, sample_xml):
        """Test main workflow with --download flag (files saved)."""
        monkeypatch.setattr(case_fetcher, "out_dir", tmp_path)
        monkeypatch.setattr('sys.argv', ['case_fetcher.py', '--download'])

        responses.add(
            responses.GET,
            f"{case_fetcher.BASE_FEED_URL}?per_page=10",
            body=sample_feed,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            body=sample_xml,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case2.xml",
            body=sample_xml,
            status=200
        )

        case_fetcher.main()

        xml_files = list(tmp_path.glob("*.xml"))
        assert len(xml_files) == 2

    @responses.activate
    def test_main_custom_per_page(self, monkeypatch, tmp_path, sample_feed, sample_xml):
        """Test main workflow with custom --per-page argument."""
        monkeypatch.setattr(case_fetcher, "out_dir", tmp_path)
        monkeypatch.setattr('sys.argv', ['case_fetcher.py', '--per-page', '25'])

        responses.add(
            responses.GET,
            f"{case_fetcher.BASE_FEED_URL}?per_page=25",
            body=sample_feed,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case1.xml",
            body=sample_xml,
            status=200
        )
        responses.add(
            responses.GET,
            "https://example.com/case2.xml",
            body=sample_xml,
            status=200
        )

        case_fetcher.main()

        assert len(responses.calls) >= 1
        assert "per_page=25" in responses.calls[0].request.url


class TestConstants:
    """Tests for module-level constants in `case_fetcher`."""

    def test_base_feed_url(self):
        """Ensure BASE_FEED_URL is correctly defined."""
        assert case_fetcher.BASE_FEED_URL == "https://caselaw.nationalarchives.gov.uk/atom.xml"

    def test_namespaces(self):
        """Ensure XML namespaces dictionary contains expected entries."""
        assert "atom" in case_fetcher.NAMESPACES
        assert "tna" in case_fetcher.NAMESPACES
        assert case_fetcher.NAMESPACES["atom"] == "http://www.w3.org/2005/Atom"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
