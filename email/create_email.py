"""This script generates an HTML email to send to subscribers."""

from datetime import datetime, timedelta
from rds_utils import get_db_connection, query_rds
from psycopg2.extensions import connection


def get_yesterdays_hearings(conn: connection) -> list[dict]:
    """Function to retrieve yesterday's hearings."""
    query = """
    SELECT
        h.hearing_citation,
        h.hearing_title,
        h.hearing_description,
        h.hearing_anomaly,
        h.hearing_url,
        j.judgement_favour
    FROM
        hearing h
    JOIN
        judgement j 
    USING(judgement_id)
    WHERE
        date(hearing_date) = (current_date - interval '1' day);
    """
    hearings = query_rds(conn, query)

    return hearings


def get_newsletter_row(hearing: dict) -> str:
    """Function to retrieve a HTML section for a given hearing."""

    html_str = """
        {hearing['citation]}
    """


def write_email(hearings: list[dict]) -> str:
    """Function to write todays comprehensive newsletter."""

    yesterdays_date = (datetime.now() - timedelta(days=1)).date()

    html = f"""<h1>Barristers Brief - Daily Report</h1>

<h2> Hearing Overview - {yesterdays_date}</h2>
    """
    html += "<p>Thanks for reading this daily update. For more details, access the <a href='http://35.179.105.252:8501'/>dashboard</a>.</p>"
    html += "<hr>"

    for hearing in hearings:
        html += "<div>"
        html += f"<h4>{hearing['hearing_citation']} - {hearing['hearing_title']}</h4>"
        html += f"<p>Ruled in favour of <b>{hearing['judgement_favour']}</b></p>"
        html += f"<p>{hearing['hearing_description']}</p>"
        if hearing['hearing_anomaly'] != 'None Found':
            html += f"<p>Anomaly: {hearing['hearing_anomaly']}</p>"
        html += f"<p>URL: <a href ='{hearing['hearing_url']}'>{hearing['hearing_url']}</a></p>"
        html += "<hr>"

        html += "</div>"
    html += "<p>From, Objection Handling</p>"

    with open(f"report_data_{yesterdays_date}.html", "w", encoding='utf-8') as f:
        f.write(html)

    return html


def get_subscriber_list(conn: connection) -> list[str]:
    """Function to get all subscribers from the RDS."""

    subscriber_list = []

    query = """
        SELECT
            email
        FROM
            subscriber;
    """

    res = query_rds(conn, query)

    if res:
        for email in res:
            subscriber_list.append(email['email'])

    return subscriber_list


def handler(context=None, event=None):
    """Handler function which runs on the lambda."""
    conn = get_db_connection()

    hearings = get_yesterdays_hearings(conn)

    subscriber_emails = get_subscriber_list(conn)
    email = write_email(hearings)

    print(subscriber_emails)
    print(email)

    conn.close()

    return {
        'subscriber_emails': subscriber_emails,
        'email': email
    }


if __name__ == "__main__":
    handler()
