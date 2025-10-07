"""File holding RDS Utility functions"""

import logging
from os import environ as ENV
from psycopg2.extensions import connection
from psycopg2 import connect, Error
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import pandas as pd


def get_db_connection():
    load_dotenv()
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
        logging.critical("Error connecting to RDS")
        return None


def query_rds(con: connection, query: str) -> dict:
    """Function to query the RDS with a given query."""
    with con.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()
    return data
