# pylint: skip-file

from os import environ as ENV

import psycopg2
from psycopg2.extensions import connection
from psycopg2.errors import Error
from dotenv import load_dotenv

from case_fetcher import case_fetcher
from xml_extraction import metadata_xml


def get_db_connection() -> connection:
    """Return a connection to a PostgreSQL database."""
    load_dotenv()
    try:
        return psycopg2.connect(
            dbname=ENV["DB_NAME"],
            host=ENV["DB_HOST"],
            port=ENV["DB_PORT"],
            user=ENV["DB_USERNAME"],
            password=ENV["DB_PASSWORD"]
        )
    except Error as e:
        raise ConnectionError(f"connection to {ENV["DB_NAME"]} failed") from e


def get_xml_strings(per_page: int = 20) -> list[str]:
    """Returns the last `per_page` transcript XMLs as strings."""
    feed = case_fetcher.fetch_feed(per_page)
    entries = case_fetcher.get_xml_entries(feed)
    xml_strings = list(case_fetcher.load_all_xml(entries).values())
    return xml_strings


def is_xml_unique(xml_string: str, conn: connection) -> bool:
    """Identifies `xml_string` by its citation, and checks if it's already in DB."""
    citation = metadata_xml.get_metadata(xml_string)["citation"]

    query = """
    SELECT * FROM hearing
    WHERE hearing_citation=%s
    """
    with conn.cursor() as cur:
        cur.execute(query, (citation,))
        result = cur.fetchone()
    return result is None


def get_unique_xmls(conn: connection, number: int) -> list[str]:
    """Fetches the last `number` XML transcripts, and returns only the uniques"""
    xml_strings = get_xml_strings(per_page=number)
    return [string for string in xml_strings if is_xml_unique(string, conn)]


if __name__ == "__main__":
    load_dotenv()
    try:
        db_conn = get_db_connection()
        unique_xmls = get_unique_xmls(db_conn)
    finally:
        # ensure that connection is always closed
        db_conn.close()
