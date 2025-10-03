# pylint: skip-file

import pytest

##### XML PARSER CONSTANTS ####

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

##### XML METADATA CONSTANTS #####

XML_METADATA = """
<akomaNtoso xmlns="http://docs.oasis-open.org/legaldocml/ns/akn/3.0" xmlns:uk="https://caselaw.nationalarchives.gov.uk/akn">
<judgment name="judgment">
<meta>
<identification source="#tna">
<FRBRWork>
<FRBRthis value="https://caselaw.nationalarchives.gov.uk/id/ukpc/2025/47"/>
<FRBRuri value="https://caselaw.nationalarchives.gov.uk/id/ukpc/2025/47"/>
<FRBRdate date="2025-09-30" name="judgment"/>
<FRBRauthor href="#ukpc"/>
<FRBRcountry value="GB-UKM"/>
<FRBRnumber value="47"/>
<FRBRname value="Fang Ankong and another v Green Elite Ltd  (Virgin Islands)"/>
</FRBRWork>
<FRBRExpression>
<FRBRthis value="https://caselaw.nationalarchives.gov.uk/ukpc/2025/47"/>
<FRBRuri value="https://caselaw.nationalarchives.gov.uk/ukpc/2025/47"/>
<FRBRdate date="2025-09-30" name="judgment"/>
<FRBRauthor href="#ukpc"/>
<FRBRlanguage language="eng"/>
</FRBRExpression>
<FRBRManifestation>
<FRBRthis value="https://caselaw.nationalarchives.gov.uk/ukpc/2025/47/data.xml"/>
<FRBRuri value="https://caselaw.nationalarchives.gov.uk/ukpc/2025/47/data.xml"/>
<FRBRdate date="2025-09-30T10:06:38" name="transform"/>
<FRBRdate date="2025-09-30T11:02:41" name="tna-enriched"/>
<FRBRauthor href="#tna"/>
<FRBRformat value="application/xml"/>
</FRBRManifestation>
</identification>
<lifecycle source="#">
<eventRef date="2025-09-30" refersTo="#judgment" source="#"/>
</lifecycle>
<references source="#tna">
<TLCOrganization eId="ukpc" href="https://www.jcpc.uk/" showAs="The Judicial Committee of the Privy Council"/>
<TLCOrganization eId="tna" href="https://www.nationalarchives.gov.uk/" showAs="The National Archives"/>
<TLCEvent eId="judgment" href="#" showAs="judgment"/>
<TLCPerson eId="fang-ankong-and-another" href="" showAs="Fang Ankong and another"/>
<TLCPerson eId="green-elite-ltd" href="" showAs="Green Elite Ltd"/>
<TLCRole eId="appellant" href="" showAs="Appellant"/>
<TLCRole eId="respondent" href="" showAs="Respondent"/>
<TLCPerson eId="judge-lord-briggs" href="/judge-lord-briggs" showAs="Lord Briggs"/>
<TLCPerson eId="judge-lord-sales" href="/judge-lord-sales" showAs="Lord Sales"/>
<TLCPerson eId="judge-lord-hamblen" href="/judge-lord-hamblen" showAs="Lord Hamblen"/>
<TLCPerson eId="judge-lord-burrows" href="/judge-lord-burrows" showAs="Lord Burrows"/>
<TLCPerson eId="judge-lord-richards" href="/judge-lord-richards" showAs="Lord Richards"/>
</references>
<proprietary source="#">
<uk:court>UKPC</uk:court>
<uk:year>2025</uk:year>
<uk:number>47</uk:number>
<uk:cite>[2025] UKPC 47</uk:cite>
<uk:parser>0.27.1</uk:parser>
<uk:hash>eba479a0f0ba3086f270d4fbc7c8a6d15a17a8f883e57a891ef10db0a281210e</uk:hash>
<uk:jurisdiction/>
<uk:tna-enrichment-engine>7.4.0</uk:tna-enrichment-engine>
</proprietary>
</meta>
</judgment>
</akomaNtoso>
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
        SUB_STYLE_HEADING,
        SUB_NON_HEADING
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


@pytest.fixture
def xml_metadata() -> bytes:
    """Returns XML string with only metadata component."""
    return XML_METADATA.encode("utf-8")
