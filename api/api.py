from dotenv import load_dotenv
from flask import Flask, request

from api_utils import (
    get_db_connection,
    get_case_by_citation,
    get_case_by_date_range,
    get_case_by_verdict,
    get_judges,
    get_judge,
    get_cases_sat_by_judge
)

load_dotenv()
api = Flask(__name__)
conn = get_db_connection()


@api.get("/")
def route_main():
    """Return a simple greeting message."""
    with open("index.html", encoding="utf-8") as f:
        html = f.read()
    return html


@api.get("/case")
def route_get_case():
    """
    Route for fetching cases.

    - Can request a specific case using its Neutral Citation Number (NCN).
    - Can batch request cases using a date range.
    - Can filter by case favour (verdict).

    Citation cannot be used with any other parameter.
    """
    citation = request.args.get("citation")
    start = request.args.get("start")
    end = request.args.get("end")
    favour = request.args.get("favour")

    # Check parameters have been passed properly
    if not any((citation, start, end, favour)):
        return {"error": True, "reason": "no parameters given"}, 400
    if citation and (start or end or favour):
        return {"error": True, "reason": "citation cannot be used other parameters"}, 400
    if (start and not end) or (end and not start):
        return {"error": True, "reason": "must provide start and end date together"}, 400

    if citation:
        return get_case_by_citation(conn, citation)

    if start and end and favour:
        date_cases, status = get_case_by_date_range(conn, start, end)
        if status >= 400:
            return date_cases, status
        favour_cases, status = get_case_by_verdict(conn, favour)
        if status >= 400:
            return favour_cases, status
        by_favour = list(filter(lambda case: case in favour_cases, date_cases))
        return by_favour, 200

    if start and end:
        return get_case_by_date_range(conn, start, end)

    if favour:
        return get_case_by_verdict(conn, favour)


@api.get("/judge")
def route_get_all_judges():
    """Route for fetching all judges."""
    return get_judges(conn), 200


@api.get("/judge/<int:judge_id>")
def route_get_judge(judge_id: int):
    """Return for fetching judge by ID."""
    return get_judge(conn, judge_id)


@api.get("/judge/<int:judge_id>/case")
def route_get_judge_cases(judge_id: int):
    """Return all cases sat by a judge."""
    return get_cases_sat_by_judge(conn, judge_id)


if __name__ == "__main__":
    api.run(host="0.0.0.0", port=5000)
