"""Script to run the daily judges & court hearing pipeline."""


# Judge extraction script
# Get unique xmls
# Pass XMLS to summary script
# Returns summary for each xml
# Package into the load script
# Insert into RDS

import os
import logging
import csv
import io
from judge_scraping import judges_rds
from xml_extraction import get_unique_xml, parse_xml, metadata_xml
from gpt import summary
from pipeline import load

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def handler(event=None, context=None) -> None:
    """Handler for AWS Lambda"""
    logging.info("Starting Courts ETL Pipeline")
    conn = get_unique_xml.get_db_connection()

    # if courts.jsonl exists, delete it
    if os.path.exists("courts.jsonl"):
        os.remove("courts.jsonl")

    # if output.jsonl exists, delete it
    if os.path.exists("output.jsonl"):
        os.remove("output.jsonl")

    logging.info("Scraping judges into RDS")
    # judges_rds.scrape_and_upload_judges()

    logging.info("Getting unique XMLs")
    unique_xmls = get_unique_xml.get_unique_xmls(conn)

    logging.info("Extracting metadata from XMLs")
    metadatas = []
    for xml in unique_xmls:
        metadatas.append(metadata_xml.get_metadata(xml))

    logging.info("Parsing transcripts")
    transcripts = []
    for xml in unique_xmls:
        headings_dict = parse_xml.get_label_text_dict(xml)
        if headings_dict is None:
            continue
        citation = metadata_xml.get_metadata(xml)["citation"]
        transcripts.append({citation: headings_dict})

    logging.info("Extracting meaningful headers.")
    meaningful_headers = summary.extract_meaningful_headers(
        transcripts, 'courts.jsonl')

    for i, items in enumerate(meaningful_headers.items()):
        citation, headers = items
        reader = csv.reader(io.StringIO(headers), quotechar="'", delimiter=',')
        headers_list = next(reader)

        orig_headings = transcripts[i][citation]
        filtered_headings = {k: v for k, v
                             in orig_headings.items() if k in headers_list}

        transcripts[i] = {citation: filtered_headings}

    logging.info("Getting summaries from GPT-API")
    summaries = summary.summarise(transcripts, "output.jsonl")

    for metadata in metadatas:
        print(metadata.get('judges'))
        hearing = summaries.get(metadata["citation"])
        if hearing:
            load.insert_into_hearing(conn, hearing, metadata)

    conn.close()


if __name__ == "__main__":
    handler()
