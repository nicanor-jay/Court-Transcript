"""Script to run the daily judges & court hearing pipeline."""

# pylint: disable=unused-argument, import-error

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
import argparse

from psycopg2.extensions import connection

from judge_scraping import judges_rds
from xml_extraction import get_unique_xml, parse_xml, metadata_xml
from gpt import summary
import load

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def reset_jsonl_file(filename: str) -> None:
    """Deletes the target files if they already exist."""
    if os.path.exists(f"/tmp/{filename}.jsonl"):
        os.remove(f"/tmp/{filename}.jsonl")


def insert_scraped_judges() -> None:
    """Scrapes judges from the judiciary website, and inserts them in the DB."""
    logging.info("Scraping judges into RDS")
    judges_rds.scrape_and_upload_judges()


def extract_and_parse_xml(xmls: list[str]) -> list[str]:
    """Function to extract xml and parse it to a list of xml strings with all the metadata."""
    logging.info("Extracting metadata from XMLs")
    metadatas = []
    for xml in xmls:
        metadatas.append(metadata_xml.get_metadata(xml))

    return metadatas


def parse_transcripts(unique_xmls: list[str]) -> list[dict]:
    """Parses the unique xmls into a list of dictionaries, each representing a hearing."""
    logging.info("Parsing transcripts")
    transcripts = []
    for xml in unique_xmls:
        headings_dict = parse_xml.get_label_text_dict(xml)
        if headings_dict is None:
            continue
        citation = metadata_xml.get_metadata(xml)["citation"]
        transcripts.append({citation: headings_dict})
    return transcripts


def extract_meaningful_headers_and_content(transcripts: list[dict], filename: str) -> list[dict]:
    """Grabs only the meaningful headers and their content from each hearing
       inside the transcripts."""
    logging.info("Extracting meaningful headers.")
    meaningful_headers = summary.extract_meaningful_headers(
        transcripts, f'/tmp/{filename}.jsonl')

    for i, items in enumerate(meaningful_headers.items()):
        citation, headers = items
        reader = csv.reader(io.StringIO(headers), quotechar="'", delimiter=',')
        headers_list = next(reader)

        orig_headings = transcripts[i][citation]
        filtered_headings = {k: v for k, v
                             in orig_headings.items() if k in headers_list}

        transcripts[i] = {citation: filtered_headings}
    return transcripts


def gpt_summarise_transcripts(conn: connection,
                              transcripts: list[dict],
                              metadatas: list[str],
                              filename: str) -> None:
    """Feeds GPT-API headers and content, and it summarises it. Data is then pushed to the DB."""
    logging.info("Getting summaries from GPT-API")
    summaries = summary.summarise(transcripts, f"/tmp/{filename}.jsonl")

    for metadata in metadatas:
        logging.info(metadata)
        logging.info(metadata.get('judges'))
        hearing = summaries.get(metadata["citation"])
        logging.info(hearing)
        if hearing:
            load.insert_into_hearing(conn, hearing, metadata)


def run_etl(number_of_transcripts: int = 20) -> None:
    """Runs the entire ETL process."""
    MEANINGFUL_HEADERS_INPUT = 'headers_input'
    SUMMARY_INPUT = 'summary_input'
    logging.info("Processing %s most recent transcripts",
                 number_of_transcripts)

    # Getting DB connection
    logging.info("Starting Courts ETL Pipeline")
    conn = get_unique_xml.get_db_connection()

    # Resetting jsonl files
    reset_jsonl_file(MEANINGFUL_HEADERS_INPUT)
    reset_jsonl_file(SUMMARY_INPUT)

    # Scraping + updating judges
    insert_scraped_judges()

    # Extracting and dealing with XMLs
    logging.info("Getting unique XMLs")
    unique_xmls = get_unique_xml.get_unique_xmls(
        conn, number=number_of_transcripts)
    logging.info("%s unique transcripts found", len(unique_xmls))
    metadatas = extract_and_parse_xml(unique_xmls)
    transcripts = parse_transcripts(unique_xmls)
    transcripts = extract_meaningful_headers_and_content(
        transcripts, MEANINGFUL_HEADERS_INPUT)

    # Summarising with GPT-API
    gpt_summarise_transcripts(conn, transcripts, metadatas, SUMMARY_INPUT)

    conn.close()


def handler(event=None, context=None) -> None:
    """Handler for AWS Lambda (on 20 files by default)."""
    run_etl(number_of_transcripts=20)


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--number", type=int,
                        help="Number of transcripts to process.")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    num_files = args.number if args.number else 20
    if num_files <= 0:
        raise ValueError("number must be a value greater than 0")
    run_etl(number_of_transcripts=num_files)
