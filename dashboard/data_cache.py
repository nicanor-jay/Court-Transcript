"""File holding functions which retrieve data from the RDS (which can be cached)."""
import datetime
from psycopg2.extensions import connection
import streamlit as st
import pandas as pd
from rds_utils import query_rds


@st.cache_data(ttl=600)  # cache for 10 min
def get_total_hearing_count(_con: connection) -> dict:
    """Gets total court hearing count."""
    query = """
    SELECT
        COUNT(*) AS total
    FROM
        hearing;
    """
    return query_rds(_con, query)


@st.cache_data(ttl=600)
def get_data_from_db(_con: connection) -> pd.DataFrame:
    """Fetches joined data from hearing, judge, court, and judgement tables."""

    with _con.cursor() as cur:
        query = """
            SELECT
                h.hearing_id,
                h.hearing_citation,
                h.hearing_title,
                h.hearing_date,
                h.hearing_description,
                h.hearing_anomaly,
                h.hearing_url,
                j.judgement_favour,
                c.court_name,
                jd.judge_id,
                jd.first_name,
                jd.middle_name,
                jd.last_name,
                t.title_name,
                jd.appointment_date
            FROM hearing h
            LEFT JOIN judgement j ON h.judgement_id = j.judgement_id
            LEFT JOIN court c ON h.court_id = c.court_id
            LEFT JOIN judge_hearing jh ON h.hearing_id = jh.hearing_id
            LEFT JOIN judge jd ON jh.judge_id = jd.judge_id
            LEFT JOIN title t ON jd.title_id = t.title_id;
        """
        cur.execute(query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=colnames)
    df = df.drop_duplicates(subset=["hearing_id"]).reset_index(drop=True)

    # Convert datetime objects to strings for Streamlit display
    for col in ['hearing_date', 'appointment_date']:
        if col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].astype(str)
            elif df[col].apply(lambda x: isinstance\
                               (x, (pd.Timestamp, datetime.date, datetime.datetime))).any():
                df[col] = df[col].astype(str)

    return df

@st.cache_data(ttl=600)
def get_summaries_for_judge(_conn: connection, judge_id: int) -> str:
    """Return a list of court transcript summaries which were overseen by a specific judge."""

    all_summary_text = ''
    query = """SELECT hearing_description FROM judge j
            JOIN judge_hearing jh 
	            USING (judge_id)
            JOIN hearing h
	            USING (hearing_id)
            WHERE judge_id = %s;"""
    
    with _conn.cursor() as cur:
        cur.execute(query, (judge_id,))
        summaries = cur.fetchall()
    
    for summary in summaries:
        all_summary_text += summary['hearing_description']
    return all_summary_text