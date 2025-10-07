# pylint: skip-file
"""
Test suite for UK Judiciary Web Scraper
Run with: pytest test_judge_scraping.py -v
"""

import pytest
from judge_scraper import (
    parse_date,
    parse_name,
    looks_like_judge,
    extract_titles,
    add_title_ids,
)

PYTEST_IGNORE_COLLECT = True


class TestParseDate:
    """Tests for date parsing function."""

    def test_full_date_formats(self):
        """Should parse full date formats into YYYY-MM-DD."""
        assert parse_date("25 December 2020") == "2020-12-25"
        assert parse_date("25 Dec 2020") == "2020-12-25"
        assert parse_date("25/12/2020") == "2020-12-25"
        assert parse_date("25-12-2020") == "2020-12-25"
        assert parse_date("2020-12-25") == "2020-12-25"

    def test_month_year_formats(self):
        """Should parse month and year into YYYY-MM-01."""
        assert parse_date("December 2020") == "2020-12-01"
        assert parse_date("Dec 2020") == "2020-12-01"

    def test_invalid_dates(self):
        """Should return None for invalid date strings."""
        assert parse_date("") is None
        assert parse_date("Not a date") is None
        assert parse_date("32/13/2020") is None

    def test_whitespace_handling(self):
        """Should strip whitespace before parsing."""
        assert parse_date("  25 December 2020  ") == "2020-12-25"


class TestParseName:
    """Tests for name parsing function."""

    def test_simple_names(self):
        """Should parse a judge name with title, first and last name."""
        result = parse_name("Judge John Smith")
        assert result["title"] == "Judge"
        assert result["first_name"] == "John"
        assert result["middle_name"] is None
        assert result["last_name"] == "Smith"

    def test_three_part_names(self):
        """Should handle a middle name in parsing."""
        result = parse_name("Sir John Michael Smith")
        assert result["title"] == "Sir"
        assert result["first_name"] == "John"
        assert result["middle_name"] == "Michael"
        assert result["last_name"] == "Smith"

    def test_post_nominals_removed(self):
        """Should strip post-nominal titles like KC, QC."""
        result = parse_name("His Honour Judge Anthony Dennis Watson KC")
        assert result["title"] == "His Honour Judge"
        assert result["first_name"] == "Anthony"
        assert result["middle_name"] == "Dennis"
        assert result["last_name"] == "Watson"

    def test_multiple_post_nominals(self):
        """Should remove multiple post-nominals."""
        result = parse_name("Judge John Smith QC")
        assert result["last_name"] == "Smith"

        result = parse_name("Sir John Smith CBE")
        assert result["last_name"] == "Smith"

    def test_surname_prefixes_van(self):
        """Should handle surname prefix 'van der' with no first name."""
        result = parse_name("His Honour Judge van der Zwart")
        assert result["title"] == "His Honour Judge"
        assert result["first_name"] is None
        assert result["middle_name"] is None
        assert result["last_name"] == "van der Zwart"

    def test_surname_prefixes_with_first_name(self):
        """Should handle surname prefix with first name."""
        result = parse_name("Judge Jan van der Berg")
        assert result["title"] == "Judge"
        assert result["first_name"] == "Jan"
        assert result["middle_name"] is None
        assert result["last_name"] == "van der Berg"

    def test_surname_prefixes_de(self):
        """Should handle surname prefix 'de la'."""
        result = parse_name("Judge Marie de la Cruz")
        assert result["first_name"] == "Marie"
        assert result["last_name"] == "de la Cruz"

    def test_surname_prefixes_von(self):
        """Should handle surname prefix 'von'."""
        result = parse_name("Judge Klaus von Stein")
        assert result["first_name"] == "Klaus"
        assert result["last_name"] == "von Stein"

    def test_complex_name_with_middle_and_prefix(self):
        """Should parse names with middle name and surname prefix."""
        result = parse_name("Judge John Michael van der Berg")
        assert result["first_name"] == "John"
        assert result["middle_name"] == "Michael"
        assert result["last_name"] == "van der Berg"

    def test_longest_title_match(self):
        """Should prefer longest matching title."""
        result = parse_name("His Honour Judge Smith")
        assert result["title"] == "His Honour Judge"

        result = parse_name("District Judge (MC) Jones")
        assert result["title"] == "District Judge (MC)"

    def test_single_name(self):
        """Should parse single judge name with no first name."""
        result = parse_name("Judge Smith")
        assert result["title"] == "Judge"
        assert result["first_name"] is None
        assert result["last_name"] == "Smith"

    def test_empty_name(self):
        """Should return None values for empty string."""
        result = parse_name("")
        assert result["title"] is None
        assert result["first_name"] is None
        assert result["last_name"] is None

    def test_various_titles(self):
        """Should correctly extract a variety of judge titles."""
        titles_to_test = [
            ("Lord Justice Smith", "Lord Justice"),
            ("Lady Justice Jones", "Lady Justice"),
            ("Sir John Smith", "Sir"),
            ("Dame Mary Jones", "Dame"),
            ("Mr John Smith", "Mr"),
            ("Mrs Jane Smith", "Mrs"),
            ("Dr John Smith", "Dr"),
        ]
        for full_name, expected_title in titles_to_test:
            result = parse_name(full_name)
            assert result["title"] == expected_title


class TestLooksLikeJudge:
    """Tests for judge detection function."""

    def test_valid_judge_names(self):
        """Should return True for valid judge titles."""
        assert looks_like_judge("Judge John Smith") is True
        assert looks_like_judge("His Honour Judge Smith") is True
        assert looks_like_judge("Lord Justice Smith") is True
        assert looks_like_judge("Sir John Smith") is True
        assert looks_like_judge("District Judge Jones") is True

    def test_invalid_judge_names(self):
        """Should return False for invalid names."""
        assert looks_like_judge("John Smith") is False
        assert looks_like_judge("123 Main Street") is False
        assert looks_like_judge("") is False

    def test_case_insensitivity(self):
        """Should accept titles regardless of case."""
        assert looks_like_judge("Judge Smith") is True
        assert looks_like_judge("judge Smith") is True
        assert looks_like_judge("sir John Smith") is True
        assert looks_like_judge("DISTRICT JUDGE Jones") is True


class TestExtractTitles:
    """Tests for title extraction function."""

    def test_extract_unique_titles(self):
        """Should return unique titles only."""
        judges = [
            {"title": "Judge", "first_name": "John"},
            {"title": "Judge", "first_name": "Jane"},
            {"title": "Sir", "first_name": "Bob"},
            {"title": "Judge", "first_name": "Alice"},
        ]
        titles = extract_titles(judges)

        assert len(titles) == 2
        title_names = [t["title_name"] for t in titles]
        assert "Judge" in title_names
        assert "Sir" in title_names

    def test_titles_have_ids(self):
        """Should assign IDs to extracted titles."""
        judges = [
            {"title": "Judge"},
            {"title": "Sir"},
        ]
        titles = extract_titles(judges)

        assert all("title_id" in t for t in titles)
        assert all(isinstance(t["title_id"], int) for t in titles)

    def test_titles_sorted_alphabetically(self):
        """Should return titles sorted alphabetically."""
        judges = [
            {"title": "Sir"},
            {"title": "Judge"},
            {"title": "Dame"},
        ]
        titles = extract_titles(judges)
        title_names = [t["title_name"] for t in titles]

        assert title_names == sorted(title_names)

    def test_empty_judges_list(self):
        """Should return empty list if no judges given."""
        titles = extract_titles([])
        assert not titles

    def test_judges_without_titles(self):
        """Should ignore judges with missing/empty titles."""
        judges = [
            {"title": None, "first_name": "John"},
            {"title": "", "first_name": "Jane"},
        ]
        titles = extract_titles(judges)
        assert len(titles) == 0


class TestAddTitleIds:
    """Tests for adding title IDs to judges."""

    def test_add_title_ids(self):
        """Should correctly map title IDs to judges."""
        judges = [
            {"title": "Judge", "first_name": "John"},
            {"title": "Sir", "first_name": "Bob"},
            {"title": "Judge", "first_name": "Jane"},
        ]
        titles = [
            {"title_id": 1, "title_name": "Judge"},
            {"title_id": 2, "title_name": "Sir"},
        ]

        add_title_ids(judges, titles)

        assert judges[0]["title_id"] == 1
        assert judges[1]["title_id"] == 2
        assert judges[2]["title_id"] == 1

    def test_missing_title_gets_none(self):
        """Should assign None if judge has no title."""
        judges = [
            {"title": None, "first_name": "John"},
        ]
        titles = [
            {"title_id": 1, "title_name": "Judge"},
        ]

        add_title_ids(judges, titles)

        assert judges[0]["title_id"] is None

    def test_unknown_title_gets_none(self):
        """Should assign None if judge's title not found."""
        judges = [
            {"title": "Unknown Title", "first_name": "John"},
        ]
        titles = [
            {"title_id": 1, "title_name": "Judge"},
        ]

        add_title_ids(judges, titles)

        assert judges[0]["title_id"] is None


class TestIntegration:
    """Integration tests for common scenarios."""

    def test_full_name_parsing_workflow(self):
        """Should parse full names with titles and post-nominals."""
        test_cases = [
            {
                "input": "His Honour Judge Anthony Dennis Watson KC",
                "expected": {
                    "title": "His Honour Judge",
                    "first_name": "Anthony",
                    "middle_name": "Dennis",
                    "last_name": "Watson",
                }
            },
            {
                "input": "His Honour Judge van der Zwart",
                "expected": {
                    "title": "His Honour Judge",
                    "first_name": None,
                    "middle_name": None,
                    "last_name": "van der Zwart",
                }
            },
            {
                "input": "Judge John Michael van den Berg QC",
                "expected": {
                    "title": "Judge",
                    "first_name": "John",
                    "middle_name": "Michael",
                    "last_name": "van den Berg",
                }
            },
        ]

        for case in test_cases:
            result = parse_name(case["input"])
            for key, value in case["expected"].items():
                assert result[key] == value, f"Failed for {case['input']}: {key}"

    def test_title_extraction_and_assignment(self):
        """Should extract titles and assign IDs consistently."""
        judges = [
            {
                "full_name": "Judge John Smith",
                "title": "Judge",
                "first_name": "John",
                "last_name": "Smith",
            },
            {
                "full_name": "Sir Bob Jones KC",
                "title": "Sir",
                "first_name": "Bob",
                "last_name": "Jones",
            },
            {
                "full_name": "Judge Jane Doe",
                "title": "Judge",
                "first_name": "Jane",
                "last_name": "Doe",
            },
        ]

        # Extract titles
        titles = extract_titles(judges)
        assert len(titles) == 2

        # Add IDs
        add_title_ids(judges, titles)

        # Verify all judges have title_id
        assert all("title_id" in j for j in judges)
        assert judges[0]["title_id"] == judges[2]["title_id"]
        assert judges[0]["title_id"] != judges[1]["title_id"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
