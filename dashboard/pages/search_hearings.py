import streamlit as st
import pandas as pd
import datetime
from data_cache import get_data_from_db
from rds_utils import get_db_connection


# Page Configuration
st.set_page_config(page_title="Search Court Hearings", layout="wide")

st.title("🔍 Search Through Court Hearings")
st.markdown("Use the filters below to explore recent hearings stored in the Court Transcripts database.")


# Load and cache data
conn = get_db_connection()
data = get_data_from_db(conn)

# Ensure consistent date formats
data["hearing_date"] = pd.to_datetime(data["hearing_date"], errors="coerce")


# Sidebar / Top Filters
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    keyword = st.text_input("Keyword Filter", placeholder="Enter keyword in title or description...")

with col2:
    court_filter = st.selectbox(
        "Court Filter",
        options=["All"] + sorted(data["court_name"].dropna().unique().tolist())
    )

with col3:
    start_date, end_date = st.date_input(
        "Date Range",
        value=(data["hearing_date"].min(), data["hearing_date"].max())
    )

with col4:
    ruling_filter = st.selectbox(
        "Ruling Favour",
        options=["All"] + sorted(data["judgement_favour"].fillna("Undisclosed").unique().tolist())
    )


# Filter Logic
filtered = data.copy()

if keyword:
    keyword_lower = keyword.lower()
    filtered = filtered[
        filtered["hearing_title"].str.lower().str.contains(keyword_lower, na=False)
        | filtered["hearing_description"].str.lower().str.contains(keyword_lower, na=False)
    ]

if court_filter != "All":
    filtered = filtered[filtered["court_name"] == court_filter]

if ruling_filter != "All":
    filtered = filtered[filtered["judgement_favour"].fillna("Undisclosed") == ruling_filter]

if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
    filtered = filtered[
        (filtered["hearing_date"].dt.date >= start_date)
        & (filtered["hearing_date"].dt.date <= end_date)
    ]


# Results Display
st.markdown(f"### Showing {len(filtered)} matching hearing(s)")

if filtered.empty:
    st.info("No hearings found matching your filters.")
else:
    for _, row in filtered.iterrows():
        with st.container(border=True):
            col_a, col_b = st.columns([5, 1])

            with col_a:
                st.markdown(f"#### {row['hearing_title'] or 'Untitled Hearing'}")
                st.markdown(
                    f"**Court:** {row['court_name'] or 'Unknown'}  "
                    f"| **Date:** {row['hearing_date'].date() if pd.notna(row['hearing_date']) else 'Unknown'}"
                )
                st.markdown(
                    f"<div style='color: #666; font-size: 0.9em; margin-top: 0.5em;'>"
                    f"{(row['hearing_description'] or '')[:300]}{'...' if row['hearing_description'] and len(row['hearing_description']) > 300 else ''}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

                if row.get("hearing_url"):
                    st.markdown(f"[🔗 View Full Hearing]({row['hearing_url']})", unsafe_allow_html=True)

            with col_b:
                ruling = row["judgement_favour"] or "Undisclosed"
                color = {
                    "Claimant": "#16a34a",
                    "Defendant": "#dc2626",
                    "Undisclosed": "#6b7280"
                }.get(ruling, "#6b7280")
                st.markdown(
                    f"<div style='background:{color}; color:white; padding:6px 12px; border-radius:8px; text-align:center;'>"
                    f"{ruling}</div>",
                    unsafe_allow_html=True
                )
