"""Utility functions for the API."""

from os import environ as ENV
from datetime import datetime

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor


def get_db_connection() -> connection:
    """Return a connection to a PostgreSQL server."""
    try:
        return psycopg2.connect(
            dbname=ENV["DB_NAME"],
            host=ENV["DB_HOST"],
            port=ENV["DB_PORT"],
            user=ENV["DB_USERNAME"],
            password=ENV["DB_PASSWORD"],
            cursor_factory=RealDictCursor
        )
    except psycopg2.errors.Error as e:
        raise ConnectionError(f"Connection to {ENV['DB_NAME']} failed") from e


def merge_cases(set_1: list[dict], set_2: list[dict]) -> list[dict]:
    """Merges two sets of cases while removing duplicates."""
    all_cases = set_1 + set_2
    seen_citations = set()
    for idx, case in enumerate(all_cases):
        if case["hearing_citation"] in seen_citations:
            del all_cases[idx]
        else:
            seen_citations.add(case["hearing_citation"])
    return all_cases


def get_case_by_citation(conn: connection, citation: str) -> tuple[dict, int]:
    """Get a case by its citation."""
    query = """
    SELECT *
    FROM HEARING
    JOIN court USING (court_id)
    JOIN judgement USING (judgement_id)
    JOIN judge_hearing USING (hearing_id)
    JOIN judge USING (judge_id)
    WHERE hearing_citation=%s
    """
    with conn.cursor() as cur:
        cur.execute(query, (citation,))
        results = cur.fetchone()
    not_found = {"error": True, "reason": f"did not locate {citation}"}, 404
    return (dict(results), 200) if results else not_found


def get_case_by_date_range(
        conn: connection,
        start: str,
        end: str
) -> tuple[list[dict], int] | tuple[dict, int]:
    """Returns all hearings that were concluded between `start` and `end` (inclusive)"""
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
    except ValueError:
        return {"error": True, "reason": "start and end must be in YYYY-MM-DD format"}, 400

    if end < start:
        return {"error": True, "reason": "end must on or before start"}, 400

    query = """
    SELECT *
    FROM HEARING
    JOIN court USING (court_id)
    JOIN judgement USING (judgement_id)
    JOIN judge_hearing USING (hearing_id)
    JOIN judge USING (judge_id)
    WHERE
        hearing_date >= %s AND
        hearing_date <= %s
    """
    with conn.cursor() as cur:
        cur.execute(query, (start_dt, end_dt))
        results = cur.fetchall()
    return list(results), 200


def get_case_by_verdict(
        conn: connection,
        favour: str
) -> tuple[list[dict], int] | tuple[dict, int]:
    """Gets cases that were in `favour` of 'plaintiff' or 'defendant'."""
    if favour not in ["plaintiff", "defendant"]:
        return {"error": True, "reason": "favour must be plaintiff or defendant"}, 400
    favour = favour.capitalize()
    query = """
    SELECT *
    FROM HEARING
    JOIN court USING (court_id)
    JOIN judgement USING (judgement_id)
    JOIN judge_hearing USING (hearing_id)
    JOIN judge USING (judge_id)
    WHERE
        judgement_favour=%s
    """
    with conn.cursor() as cur:
        cur.execute(query, (favour,))
        results = cur.fetchall()
    return list(results), 200
