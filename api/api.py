from dotenv import load_dotenv
from flask import Flask, request

from api_utils import (
    get_db_connection,
    get_case_by_citation,
    get_case_by_date_range
)

load_dotenv()
api = Flask(__name__)
conn = get_db_connection()


@api.get("/")
def route_main():
    """Return a simple greeting message."""
    return "Hello there."


@api.get("/case")
def route_get_case():
    """
    Route for fetching cases.

    - Can request a specific case using its Neutral Citation Number (NCN).
    - Can batch request cases using a date range.

    Citation cannot be used with any other parameter.
    """
    citation = request.args.get("citation")
    start = request.args.get("start")
    end = request.args.get("end")

    # Check parameters have been passed properly
    if not any((citation, start, end)):
        return {"error": True, "reason": "no parameters given"}, 400
    if citation and (start or end):
        return {"error": True, "reason": "citation cannot be used other parameters"}, 400
    if (start and not end) or (end and not start):
        return {"error": True, "reason": "must provide start and end date together"}, 400

    if citation:
        return get_case_by_citation(conn, citation)

    if start and end:
        return get_case_by_date_range(conn, start, end)


if __name__ == "__main__":
    api.run(port=8000)
