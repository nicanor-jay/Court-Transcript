from os import environ as ENV

import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.errors import Error
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()
api = Flask(__name__)
try:
    conn = psycopg2.connect(
        dbname=ENV["DB_NAME"],
        host=ENV["DB_HOST"],
        port=ENV["DB_PORT"],
        user=ENV["DB_USERNAME"],
        password=ENV["DB_PASSWORD"],
        cursor_factory=RealDictCursor
    )
except Error as e:
    raise ConnectionError(f"Connection to {ENV['DB_NAME']} failed") from e


@api.get("/")
def route_main():
    """Return a simple greeting message."""
    return "Hello there."


@api.get("/case")
def route_get_case():
    """Get a case by its citation."""
    citation = request.args.get("citation")
    if citation is None:
        return {"error": True, "reason": "citation must be provided"}
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
    not_found = {"error": True, "reason": f"did not locate {citation}"}
    return dict(results) if results else not_found


if __name__ == "__main__":
    api.run(port=5000)
