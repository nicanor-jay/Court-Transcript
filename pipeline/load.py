"""This script loads data into the hearing table as well as the judge_hearing table."""

from os import environ as ENV
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import Error


from judge_scraping.judge_scraper import parse_name


def get_db_connection() -> connection:
    """ Returns a connection to our database. """
    try:
        db_connection = connect(
            host=ENV['DB_HOST'],
            user=ENV['DB_USERNAME'],
            password=ENV['DB_PASSWORD'],
            database=ENV['DB_NAME']
        )
        return db_connection
    except Error as e:
        # print(f"Error connecting to database: {e}")
        return None


def get_title_id(conn: connection, title_name: str) -> int:
    """ Returns the title ID that matches the given judge title. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT title_id
        FROM title
        WHERE title_name = %s;
        """

        cur.execute(query, title_name)
        return cur.fetchone()


def check_judge_exists(conn: connection, judges: list) -> list[int]:
    """ Returns the judge_id if the judge exists in the judge table. """

    judge_ids = []
    for judge in judges:
        judge = parse_name(judge)
        title_id = get_title_id(conn, judge['title'])
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            SELECT id
            FROM judge
            WHERE title_id = %s
            AND last_name = %s;
            """
            cur.execute(query, (title_id, judge.get('last_name')))
            judge_ids.append(cur.fetchone()[0])

    return [id for id in judge_ids if id is not None]


def get_judgement_id(conn: connection, ruling: str) -> int:
    """ Returns the judgement ID that matches the ruling. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT judgement_id
        FROM judgement
        WHERE judgement_favour = %s;
        """

        cur.execute(query, ruling)
        result = cur.fetchone()
    return result


def get_court_id(conn: connection, court_name: str) -> int:
    """ Returns the court ID for a given court name. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT court_id
        FROM court
        WHERE court_name = %s;
        """

        cur.execute(query, court_name)
        return cur.fetchone()


def insert_into_court(conn: connection, court: str) -> int:
    """ Insert a a new row into the court table and return its id. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        INSERT INTO court (court_name)
        VALUES (%s)
        RETURNING id;
        """  # may need to change id to court_id (find out after testing)
        cur.execute(query, court)
        conn.commit()

    return cur.fetchone()


def insert_into_judge_hearing(conn: connection, judge_ids: list, hearing_id: int) -> None:
    """ Inserts records in the judge_hearing table. """

    for judge_id in judge_ids:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            INSERT INTO judge_hearing (judge_id, hearing_id)
            VALUES (%s, %s);
            """
            cur.execute(query, (judge_id, hearing_id,))
            conn.commit()


def insert_into_hearing(conn: connection, hearing: dict, metadata: dict) -> None:
    """ Inserts a new row in the hearing table. """
    judge_ids = check_judge_exists(conn, metadata.get('judges'))
    if judge_ids:
        judgement_id = get_judgement_id(conn, hearing.get('ruling'))
        court_id = get_court_id(conn, metadata.get('court'))
        if court_id is None:
            court_id = insert_into_court(conn, metadata.get('court'))
        hearing_title = metadata.get('title')
        hearing_date = metadata.get('verdict_date')
        citation = metadata.get('citation')
        description = hearing.get('summary')
        anomaly = hearing.get('anomaly')
        hearing_url = metadata.get('url')

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            INSERT INTO hearing
            (judgement_id, court_id, case_number, hearing_title, hearing_date, hearing_description, hearing_url, hearing_anomaly)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
            cur.execute(query, (judgement_id, court_id, citation,
                        hearing_title, hearing_date, description, hearing_url, anomaly))
            hearing_id = cur.fetchone()
            conn.commit()
        insert_into_judge_hearing(conn, judge_ids, hearing_id)
