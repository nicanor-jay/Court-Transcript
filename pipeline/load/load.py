from os import environ as ENV
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from psycopg2 import Error



def get_db_connection() -> connection:
    """ Returns a connection to our database. """
    try:
        connection = connect(
            host=ENV['DB_HOST'],
            user=ENV['DB_USERNAME'],
            password=ENV['DB_PASSWORD'],
            database=ENV['DB_NAME']
        )
        return connection
    except Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_title_id(title_name: str) -> int:
    """ Returns the title ID that matches the given judge title. """
    conn = get_db_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT title_id
        FROM title
        WHERE title_name = %s;
        """
        
        cur.execute(query, title_name)
        return cur.fetchone()

def check_judge_exists(metadata: dict) -> int:
    """ Returns true if the judge exists in the judge table. """ 

    title_id = get_title_id(metadata.get('title'))
    conn = get_db_connection()
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT id
        FROM judge
        WHERE title_id = %s
        AND last_name = %s;
        """

        cur.execute(query, (title_id, metadata.get('last_name')))
        return cur.fetchone()[0]
    


def get_judgement_id(ruling: str) -> int:
    """ Returns the judge ID that matches the ruling. """
    if ruling == "Not Found":
        return None
    
    conn = get_db_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT judgement_id
        FROM judgement
        WHERE judgement_favour = %s;
        """
        
        cur.execute(query, ruling)
        return cur.fetchone()


def get_court_id(court_name: str) -> int:
    """ Returns the court ID for a given court name. """

    conn = get_db_connection()
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        SELECT court_id
        FROM court
        WHERE court_name = %s;
        """

        cur.execute(query, court_name)
        return cur.fetchone()


def insert_into_judgement(ruling: str) -> int:
    """ Insert a a new row into the judgement table and return its id. """

    conn = get_db_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        INSERT INTO judgement (judgement_favour)
        VALUES (%s)
        RETURNING id;
        """ # may need to change id to judgement_id (find out after testing)
        cur.execute(query, ruling)
        conn.commit()

    return cur.fetchone()


def insert_into_court(court: str) -> int:
    """ Insert a a new row into the court table and return its id. """
    conn = get_db_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        INSERT INTO court (court_name)
        VALUES (%s)
        RETURNING id;
        """  # may need to change id to court_id (find out after testing)
        cur.execute(query, court)
        conn.commit()

    return cur.fetchone()


def insert_into_judge_hearing(judge_id, hearing_id) -> None:
    """ Inserts records in the judge_hearing table. """
    conn = get_db_connection()

    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        query = """
        INSERT INTO judge_hearing (judge_id, hearing_id)
        VALUES (%s, %s);
        """
        cur.execute(query, (judge_id, hearing_id,))
        conn.commit()



def insert_into_hearing(hearing: dict, metadata: dict) -> None:
    """ Inserts a new row in the hearing table. """
    judge_id = check_judge_exists(metadata.get('judge'))
    if judge_id:
        judgement_id = get_judgement_id(hearing.get(('ruling')))
        if judgement_id is None:
            judgement_id = insert_into_judgement(hearing.get('ruling'))
        court_id = get_court_id(metadata.get('court'))
        if court_id is None:
            court_id = insert_into_court(metadata.get('court'))
        hearing_title = metadata.get('title')
        hearing_date = metadata.get('verdict_date')
        citation = metadata.get('citation')
        description = hearing.get('summary')
        anomaly = hearing.get('anomaly')
        hearing_url = metadata.get('url')

        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            query = """
            INSERT INTO hearing
            (judgement_id, court_id, case_number, hearing_title, hearing_date, hearing_description, hearing_url, hearing_anomaly)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
            """
            cur.execute(query, (judgement_id, court_id, citation, hearing_title, hearing_date, description, hearing_url, anomaly))
            hearing_id = cur.fetchone()
            conn.commit()
        insert_into_judge_hearing(judge_id, hearing_id)
    

if __name__ == "__main__":
    load_dotenv()


# [{"transcript-1": {
#     "summary": [a concise description of what the hearing was about, maximum 1000 characters],
#     "ruling": [which party the court ruled in favour of(one word answer e.g. Defendant)],
#     "anomaly": [whether anything irregular happened in the context of a normal court hearing]
# }}]
