"""Script to run the daily judges & court hearing pipeline."""


# Judge extraction script
# Get unique xmls
# Pass XMLS to summary script
# Returns summary for each xml
# Package into the load script
# Insert into RDS

import os
import csv
import io
from judge_scraping import rds_utils
from judge_scraping import judge_scraper
from judge_scraping import judges_rds
from xml_extraction import get_unique_xml, parse_xml, metadata_xml
from gpt import summary


def handler(event=None, context=None) -> None:
    """Handler for AWS Lambda"""
    conn = get_unique_xml.get_db_connection()

    # if courts.jsonl exists, delete it
    if os.path.exists("courts.jsonl"):
        os.remove("courts.jsonl")

    # judges_rds.scrape_and_upload_judges()
    unique_xmls = get_unique_xml.get_unique_xmls(conn)

    transcripts = []
    for xml in unique_xmls:
        headings_dict = parse_xml.get_label_text_dict(xml)
        if headings_dict is None:
            continue
        citation = metadata_xml.get_metadata(xml)["citation"]
        transcripts.append({citation: headings_dict})

    meaningful_headers = summary.extract_meaningful_headers(
        transcripts, 'courts.jsonl')

    # {"citation-1": "'hello','hi','reading','verdict'",
    # "citation-2": "'hello','hi','reading','verdict'"}

    # meaning_texts = []
    # for citation, headers in meaningful_headers.items():
    #     reader = csv.reader(io.StringIO(headers), quotechar="'", delimiter=',')
    #     headers_list = next(reader)

    # transcript_meaningful_text = {}
    # for header in headers_list:
    #     text = transcripts[citation][header]
    #     transcript_meaningful_text[header] = text
    # meaning_texts.append(transcript_meaningful_text)

    # transcription
    # [{"citation": {
    #  label: text,
    #  label: text
    #  }
    # }]

    for i, items in enumerate(meaningful_headers.items()):
        citation, headers = items
        reader = csv.reader(io.StringIO(headers), quotechar="'", delimiter=',')
        headers_list = next(reader)

        orig_headings = transcripts[i][citation]
        filtered_headings = {k: v for k, v
                             in orig_headings.items() if k in headers_list}

        transcripts[i] = {citation: filtered_headings}

    print(summary.summarise(transcripts, "output.jsonl"))

    conn.close()


if __name__ == "__main__":
    handler()
