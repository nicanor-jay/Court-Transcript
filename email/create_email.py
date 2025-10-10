"""This script generates an HTML email to send to subscribers."""

import logging
from datetime import datetime, timedelta
from aws_utils import get_db_connection, query_rds
from psycopg2.extensions import connection

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


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


def write_email(hearings: list[dict]) -> str:
    """Function to write todays comprehensive newsletter."""

    yesterdays_date = (datetime.now() - timedelta(days=1)).date()

    plaintiff_count = sum([
        1 for hearing in hearings if hearing['judgement_favour'] == 'Plaintiff'])
    defendant_count = len(hearings) - plaintiff_count

    html = f"""
    <html>
        <body style="font-family: 'Trebuchet MS', sans-serif; background-color: #212838; color: #ead9d6";>
        <img src="images/courtlogo.png" alt="Team logo" style="float: left; width: 80px; height: 80px;">
        <h2 style="color: #b29758; position: relative; top: 18px; left: 10px;"> Hearing Overview - {yesterdays_date}</h2>
        <br>
        <br>
        <div>Thanks for reading this daily update. For more details, access the <a href='http://18.175.52.45:8501' style="color: #238fb5;">dashboard</a>.</div>
        
        <hr>
        <p>Total Cases: {len(hearings)}</p>
        <p>In Favour of Plaintiff: {plaintiff_count}</p>
        <p>In Favour of Defendant: {defendant_count}</p>
        <hr>

        <h2 style="color: #b29758;">Hearings</h2>
    """

    for hearing in hearings:
        html += f"""
        <div>
            <h4>{hearing['hearing_citation']} - {hearing['hearing_title']}</h4>
            <p>Ruled in favour of <b>{hearing['judgement_favour']}</b></p>
            <p>{hearing['hearing_description']}</p>
        """
        if hearing['hearing_anomaly'] != 'None Found':
            html += f"<p>Anomaly: {hearing['hearing_anomaly']}</p>"
        html += f"""
            <p>URL: <a href ='{hearing['hearing_url']}'>{hearing['hearing_url']} style="color: #238fb5;"</a></p>
            <hr>

        </div>
        <p>From, Objection Handling</p>
        """

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


def get_subscribers_and_email():
    """Gets subscribers email list and HTML email template."""
    conn = get_db_connection()

    hearings = get_yesterdays_hearings(conn)

    logging.info("Getting subscribers and email template.")
    subscriber_emails = get_subscriber_list(conn)
    email = write_email(hearings)

    conn.close()

    res = {
        'subscriber_emails': subscriber_emails,
        'email': email
    }

    return res


def handler(context=None, event=None):
    """Handler function which runs on the lambda."""
    return get_subscribers_and_email()


if __name__ == "__main__":
    handler()
