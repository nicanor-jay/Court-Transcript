"""This script loads data into the hearing table as well as the judge_hearing table."""

import logging
from os import environ as ENV
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import Error


from judge_scraping.judge_scraper import parse_name

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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
        print(f"Error connecting to database: {e}")
        return None


def get_title_id(conn: connection, title_name: str) -> int:
    """ Returns the title ID that matches the given judge title. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT title_id
        FROM title
        WHERE LOWER(title_name) = LOWER(%s);
        """

        cur.execute(query, (title_name,))
        data = cur.fetchone()
        return data.get('title_id') if data else None


def insert_title_id(conn: connection, title_name: str) -> int:
    """Inserts new titles into title table."""
    with conn.cursor() as cur:
        query = """
            INSERT INTO
                title(title_name)
            VALUES(%s)
            RETURNING title_id;
        """
        cur.execute(query, (title_name,))
        inserted_id = cur.fetchone()[0]
        conn.commit()
        logging.info("Inserted Title: %s", title_name)

    return inserted_id


def insert_judges(conn: connection, judges: list) -> list[int]:
    """Inserts judges & returns their ids."""
    judge_ids = []
    if judges:
        for judge in judges:

            name = parse_name(judge)
            title_id = get_title_id(conn, name['title'])

            if not title_id and name['title']:
                title_id = insert_title_id(conn, name['title'])

            with conn.cursor() as cur:
                query = """
                    INSERT INTO
                        judge(title_id, first_name, middle_name, last_name, appointment_date)
                    VALUES(%s, %s, %s, %s, %s)
                    ON CONFLICT (title_id, first_name, middle_name, last_name, appointment_date) DO NOTHING
                    RETURNING judge_id;
                    """
                cur.execute(query, (title_id, name.get(
                    'first_name'), name.get('middle_name'), name.get('last_name'), None))
                data = cur.fetchone()
                if data:
                    judge_ids.append(data[0])
                    logging.info("Inserted Judge: %s with ID: %s",
                                 name.get('last_name'), data[0])
                else:
                    logging.info("Response is None.")
                conn.commit()
    return judge_ids


def check_judge_exists(conn: connection, judges: list) -> list[int]:
    """ Returns the judge_id if the judge exists in the judge table. """

    judge_ids = []
    if judges:
        for judge in judges:
            judge = parse_name(judge)
            title_id = get_title_id(conn, judge['title'])
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # query = """
                # SELECT judge_id
                # FROM judge
                # WHERE title_id = %s
                # AND LOWER(last_name) = LOWER(%s);
                # """

                # Dumbed down check
                query = """
                SELECT judge_id
                FROM judge
                WHERE LOWER(last_name) = LOWER(%s);
                """

                # cur.execute(query, (title_id, judge.get('last_name')))
                cur.execute(query, (judge.get('last_name'),))
                data = cur.fetchone()
                if data:
                    logging.info(
                        "Judge ID %s found. Appending to judge_ids", data['judge_id'])
                    judge_ids.append(data['judge_id'])

    return judge_ids


def get_judgement_id(conn: connection, ruling: str) -> int:
    """ Returns the judgement ID that matches the ruling. """
    if ruling.lower() not in ['plaintiff', 'defendant', 'undisclosed']:
        return None

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT judgement_id
        FROM judgement
        WHERE LOWER(judgement_favour) = LOWER(%s);
        """

        cur.execute(query, (ruling,))
        result = cur.fetchone()['judgement_id']
    return result


def get_court_id(conn: connection, court_name: str) -> int:
    """ Returns the court ID for a given court name. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT court_id
        FROM court
        WHERE LOWER(court_name) = LOWER(%s);
        """

        cur.execute(query, (court_name,))
        data = cur.fetchone()
        return data['court_id'] if data else None
        # return cur.fetchone()['court_id']


def insert_into_court(conn: connection, court: str) -> int:
    """ Insert a a new row into the court table and return its id. """

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        INSERT INTO court (court_name)
        VALUES (%s)
        RETURNING court_id;
        """  # may need to change id to court_id (find out after testing)
        cur.execute(query, (court,))
        conn.commit()
        return cur.fetchone()['court_id']


def insert_into_judge_hearing(conn: connection, judge_ids: list, hearing_id: int) -> None:
    """ Inserts records in the judge_hearing table. """

    for judge_id in judge_ids:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            INSERT INTO judge_hearing (judge_id, hearing_id)
            VALUES (%s, %s);
            """
            cur.execute(query, (judge_id, hearing_id))
            logging.info("Inserting judge hearing: %s, %s...",
                         judge_id, hearing_id)
            conn.commit()
            logging.info("Inserted judge hearing: %s, %s",
                         judge_id, hearing_id)


def insert_into_hearing(conn: connection, hearing: dict, metadata: dict) -> None:
    """ Inserts a new row in the hearing table. """
    if not metadata.get('judges'):
        # Skip if judges is None
        logging.info('Skipping %s - No Judges', metadata.get("citation"))
        return

    if not get_judgement_id(conn, hearing.get('ruling')):
        logging.info('Skipping. No conclusive judgement found.')
        return

    judge_ids = check_judge_exists(conn, metadata.get('judges'))

    if len(judge_ids) != len(metadata.get('judges')):
        judge_ids += insert_judges(conn, metadata.get('judges'))

    logging.info("Judge IDs: %s", judge_ids)

    logging.info("Ruling: %s", hearing.get('ruling'))

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

    logging.info("Hearing Title: %s", hearing_title)
    logging.info("Hearing Date: %s", hearing_date)
    logging.info("Citation: %s", citation)
    logging.info("Description: %s", description[:100])
    logging.info("Anomaly: %s", anomaly[:100])
    logging.info("Hearing URL: %s", hearing_url)

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        INSERT INTO hearing
        (judgement_id, court_id, hearing_citation, hearing_title, hearing_date, hearing_description, hearing_url, hearing_anomaly)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING hearing_id;
        """
        cur.execute(query, (judgement_id, court_id, citation,
                    hearing_title, hearing_date, description, hearing_url, anomaly))
        hearing_id = cur.fetchone()['hearing_id']
        logging.info("Inserting hearing: %s...", citation)
        conn.commit()
        logging.info("Inserted hearing: %s", citation)
    insert_into_judge_hearing(conn, judge_ids, hearing_id)
