# pylint: skip-file

from os import environ as ENV

import psycopg2
from psycopg2.extensions import connection
from psycopg2.errors import Error
from dotenv import load_dotenv
from lxml import etree

from metadata_xml import get_metadata
import path_bootstrap_util


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
    feed = fetch_feed(20)
    entries = get_xml_entries(feed)
    xml_strings = list(load_all_xml(entries).values())
    return xml_strings


def is_xml_unique(xml_string: str, conn: connection) -> bool:
    """Identifies `xml_string` by its citation, and checks if it's already in DB."""
    citation = get_metadata(xml_string)["citation"]

    query = """
    SELECT * FROM hearing
    WHERE court_id=%s
    """
    with conn.cursor() as cur:
        cur.execute(query, (citation,))
        result = cur.fetchone()
    return result is None


def get_unique_xmls(conn: connection) -> list[str]:
    """Fetches the last 20 XML transcripts, and returns only the uniques"""
    xml_strings = get_xml_strings()
    return [string for string in xml_strings if is_xml_unique(string, conn)]


if __name__ == "__main__":
    load_dotenv()
    db_conn = get_db_connection()
    unique_xmls = get_unique_xmls(db_conn)
