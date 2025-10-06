"""This script uploads any new judges from from webscraping up to the RDS."""

import json
import logging
import subprocess
from typing import Optional
from psycopg2.extensions import connection
from judge_scraping.rds_utils import get_db_connection, query_rds

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# pylint:disable=too-many-arguments,too-many-positional-arguments

# STEPS
# Get all judges from webscraping scripts
# Attempt to insert the title
# Try to insert title
# If exists, get the inserted_id
# If not exists, insert title and keep the inserted_id
# Attempt to insert judge
# If no duplicates found across first_name, middle_name, last_name, appointment_date
# Insert Judge
# Else
# PSQL will deny, then we can skip


def get_judges_from_rds(conn: connection):
    """Get existing judges from RDS."""
    exists = query_rds(conn, "SELECT * FROM judge;")
    logging.info("Found %s existing judges in RDS", len(exists))
    return exists


def run_scraper():
    """Run the judge scraping script."""
    logging.info("Running scraper")
    subprocess.run(["python3", "judge_scraping.py"], check=True)
    logging.info("Completed scraping. ")


def load_scraped_judges():
    """Load judges from JSON file. """
    with open("judges_data.json", "r", encoding="utf-8") as f:
        judges = json.load(f)
    logging.info("Loaded %s judges from scraper.", len(judges))
    return judges


def get_title_id(conn: connection, title_name: str) -> Optional[int]:
    """Get title_id for given title."""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                title_id
            FROM
                title
            WHERE
                title_name = %s
        """, (title_name,))
        data = cur.fetchone()
        inserted_id = data['title_id'] if data else None
    return inserted_id


def insert_title(conn: connection, title_name: str) -> Optional[int]:
    """Inserts any new titles into the title table."""
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO
                title (title_name)
            VALUES(%s)
            ON CONFLICT (title_name) DO NOTHING
            RETURNING title_id;
        """, (title_name,))
        data = cur.fetchone()
        inserted_id = data['title_id'] if data else None
        conn.commit()
    return inserted_id


def insert_judge(con: connection,
                 title_id: int,
                 first_name: str,
                 middle_name: str,
                 last_name: str,
                 appointment_date: str) -> Optional[int]:
    """Inserts any new judges into the judge table."""
    query = """
        INSERT INTO
            judge (title_id, first_name, middle_name, last_name, appointment_date)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (title_id, first_name, middle_name, last_name, appointment_date) DO NOTHING
        RETURNING judge_id;
    """
    with con.cursor() as cur:
        cur.execute(
            query, (title_id, first_name, middle_name,
                    last_name, appointment_date)
        )
        data = cur.fetchone()
        inserted_id = data['judge_id'] if data else None
        con.commit()
    if inserted_id:
        logging.info("Inserted new judge with ID: %s", inserted_id)
        return inserted_id
    logging.info("Not inserting - Duplicate judge")
    return None


def scrape_and_upload_judges():
    """Runs the main algorithm to scrape judges, insert titles, and insert judges."""
    con = get_db_connection()

    run_scraper()
    scraped_judges = load_scraped_judges()

    for judge in scraped_judges:
        title_id = get_title_id(con, judge['title'])

        if not title_id:
            # Title doesn't exist in RDS, so Load it
            title_id = insert_title(con, judge['title'])

        # Insert judge

        insert_judge(con,
                     title_id,
                     judge['first_name'],
                     judge['middle_name'],
                     judge['last_name'],
                     judge['appointment_date'])

    logging.info("All judges loaded!")

    con.close()


if __name__ == "__main__":
    scrape_and_upload_judges()
