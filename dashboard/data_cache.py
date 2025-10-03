"""File holding functions which retrieve data from the RDS (which can be cached)."""
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
