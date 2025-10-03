"""
Pytest fixtures for case_fetcher tests.

This module provides shared test data as fixtures that can be used
across all test modules in the test suite.
"""

import pytest


@pytest.fixture
def sample_feed():
    """Sample Atom feed XML for testing."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:tna="https://caselaw.nationalarchives.gov.uk">
    <entry>
        <title>Sample Case v Another Case [2024] UKSC 1</title>
        <tna:uri>https://caselaw.nationalarchives.gov.uk/id/uksc/2024/1</tna:uri>
        <link type="application/akn+xml" href="https://example.com/case1.xml"/>
    </entry>
    <entry>
        <title>Test Case [2024] EWCA 100</title>
        <tna:uri>https://caselaw.nationalarchives.gov.uk/id/ewca/2024/100</tna:uri>
        <link type="application/akn+xml" href="https://example.com/case2.xml"/>
    </entry>
    <entry>
        <title>No XML Case [2024] EWHC 50</title>
        <tna:uri>https://caselaw.nationalarchives.gov.uk/id/ewhc/2024/50</tna:uri>
    </entry>
</feed>
"""


@pytest.fixture
def sample_xml():
    """Sample XML case content for testing."""
    return """<?xml version="1.0" encoding="UTF-8"?>
<akomaNtoso>
    <judgment>Test judgment content</judgment>
</akomaNtoso>
"""
