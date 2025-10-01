"""File holding RDS Utility functions"""

import logging
from os import environ as ENV
from psycopg2.extensions import connection
from psycopg2 import connect, Error
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import pandas as pd


def get_db_connection():
    """Gets the db connection and returns it."""
    try:
        con = connect(
            host=ENV["DB_HOST"],
            database=ENV["DB_NAME"],
            user=ENV["DB_USERNAME"],
            password=ENV["DB_PASSWORD"],
            port=ENV["DB_PORT"],
            cursor_factory=RealDictCursor,
        )
        logging.info("Connected to RDS.")
        return con
    except Error as e:
        print(f"Error connecting to database: {e}")
        logging.critical("Error connecting to RDS")
        return None


def query_rds(con: connection, query: str) -> pd.DataFrame:
    """Function to query the RDS with a given query."""
    df = pd.read_sql(query, con)
    return df


def get_total_hearing_count(con: connection) -> pd.DataFrame:
    """Gets total court hearing count."""
    query = """
    SELECT
        COUNT(*)
    FROM
        hearing;
    """
    return query_rds(con, query)


if __name__ == "__main__":
    load_dotenv()
    conn = get_db_connection()

    print(query_rds(conn, "select * from information_schema.tables"))
    print(get_total_hearing_count(conn))

    conn.close()
