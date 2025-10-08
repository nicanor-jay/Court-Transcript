"""
charts.py
Functions to take in a DataFrame as argument and return Altair charts
for usage in the Streamlit dashboard.
"""

import altair as alt
import pandas as pd
import datetime
from psycopg2 import connect


def get_data_from_db(conn: connect) -> pd.DataFrame:
    """Fetches joined data from hearing, judge, court, and judgement tables."""

    with conn.cursor() as cur:
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
            elif df[col].apply(lambda x: isinstance(x, (pd.Timestamp, datetime.date, datetime.datetime))).any():
                df[col] = df[col].astype(str)
                 
    return df


def get_overall_ruling_bias_chart(data: pd.DataFrame):
    """Donut chart showing favour (Claimant vs Defendant vs Undisclosed)."""
    data['judgement_favour'] = data['judgement_favour'].fillna('Undisclosed')
    counts = data['judgement_favour'].value_counts().reset_index()
    counts.columns = ['judgement_favour', 'count']

    chart = alt.Chart(counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="judgement_favour", type="nominal", title="Ruling Favour"),
        tooltip=['judgement_favour', 'count']
    ).properties(width=250, height=250, title="Overall Ruling Bias")

    return chart


def get_recent_hearings_table(data: pd.DataFrame):
    """Display last 3–5 hearings chronologically."""
    recent = data.sort_values(by='hearing_date', ascending=False).head(5)
    table = recent[['hearing_date', 'court_name', 'hearing_title', 'judgement_favour', 'hearing_url', 'hearing_citation']]

    table = table.rename(columns={
        'hearing_citation': 'Citation',
        'hearing_date': 'Date',
        'court_name': 'Court',
        'hearing_title': 'Case Title',
        'judgement_favour': 'Ruling Favour',
        'hearing_url': 'Source URL'
    })
    return table


def get_rulings_by_court_chart(data: pd.DataFrame):
    """Stacked bar chart showing ruling by court."""
    data['judgement_favour'] = data['judgement_favour'].fillna('Undisclosed')
    chart = alt.Chart(data).mark_bar().encode(
        y=alt.Y('court_name:N', title='Court'),
        x=alt.X('count():Q', title='Number of Hearings'),
        color=alt.Color('judgement_favour:N', title='Ruling Favour'),
        tooltip=['court_name', 'count()']
    ).properties(title="Recent Rulings across Different Courts")

    return chart
