"""
main.py
Streamlit dashboard layout for court hearings data.
"""

import streamlit as st
from dotenv import load_dotenv
from rds_utils import get_db_connection
from charts import (
    get_data_from_db,
    get_recent_hearings_table,
    get_rulings_by_court_chart,
    get_overall_ruling_bias_chart,
    get_rulings_by_title,
)


def main():
    load_dotenv()
    st.set_page_config(page_title="Court Hearings Dashboard", layout="wide")

    # Connect to database
    conn = get_db_connection()

    # Load data
    data = get_data_from_db(conn)

    # Layout
    st.title("Court Hearings Overview")

    # Main content and sidebar layout
    col_main, col_side = st.columns([3, 1])

    with col_main:
        st.markdown("### Last 3–5 Court Hearings Chronologically")
        st.dataframe(get_recent_hearings_table(data), use_container_width=True)

        st.markdown("### Recent Rulings across Different Courts")
        st.altair_chart(get_rulings_by_court_chart(data), use_container_width=True)

        st.markdown("### Rulings by Judicial Title")
        st.altair_chart(get_rulings_by_title(data), use_container_width=True)

    with col_side:
        st.markdown("### Overall Ruling Bias")
        st.altair_chart(get_overall_ruling_bias_chart(data), use_container_width=True)


if __name__ == "__main__":
    main()
