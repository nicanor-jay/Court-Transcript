# pylint: skip-file

import pytest

XML_TEMPLATE = """
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0">
<judgment name="judgment">
<judgmentBody>
<decision>
{0}
{1}
{2}
{3}
</decision>
</judgmentBody>
</judgment>
</akomaNtoso>
"""

LEVEL_STYLE_HEADING = """
<level eId="lvl_1">
<content>
<p class="Paraheading6">The facts</p>
</content>
</level>
"""

LEVEL_NON_HEADING = """
<level>
<content>
<p class="Quote">And if there has been an unjustified</p>
</content>
</level>
"""

SUB_STYLE_HEADING = """
<subparagraph>
<content>
<p class="ParaLevel1">The legal framework:</p>
</content>
</subparagraph>
"""

SUB_NON_HEADING = """
<subparagraph>
<num style="font-size:13pt;margin-left:0.5in">(i)</num>
<content>
<p class="ParaApprovedLevel2">Whether the payments by Mr</p>
</content>
</subparagraph>
"""


@pytest.fixture
def xml_all_headings() -> bytes:
    """Returns XML string with, and only with, all known heading types."""
    return XML_TEMPLATE.format(
        LEVEL_STYLE_HEADING,
        LEVEL_STYLE_HEADING,
        SUB_STYLE_HEADING,
        SUB_STYLE_HEADING
    ).encode("utf-8")


@pytest.fixture
def xml_natural_file() -> bytes:
    """Returns XML string containing headings and non-headings."""
    return XML_TEMPLATE.format(
        LEVEL_STYLE_HEADING,
        LEVEL_NON_HEADING,
        SUB_NON_HEADING,
        SUB_STYLE_HEADING
    ).encode("utf-8")


@pytest.fixture
def xml_no_headings() -> bytes:
    """Returns XML string without headings."""
    return XML_TEMPLATE.format(
        SUB_NON_HEADING,
        LEVEL_NON_HEADING,
        SUB_NON_HEADING,
        LEVEL_NON_HEADING
    ).encode("utf-8")


@pytest.fixture
def xml_reverse_order() -> bytes:
    """
    Returns XML string with SUB headings occurring before LEVEL headings.

    This is useful when testing if element ordering is retained.
    """
    return XML_TEMPLATE.format(
        SUB_NON_HEADING,
        SUB_STYLE_HEADING,
        LEVEL_STYLE_HEADING,
        LEVEL_NON_HEADING
    ).encode("utf-8")
