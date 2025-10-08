#pylint:disable=line-too-long, import-error
"""Streamlit dashboard page for searching hearings. """
import datetime
import streamlit as st
import pandas as pd
from data_cache import get_data_from_db
from rds_utils import get_db_connection

# --- CSS INJECTION FOR GOLD HEADERS & JUDGE DETAILS HIDDEN
GOLD_COLOR = "#b29758"
SECONDARY_GOLD_COLOUR = "#a38c64"

st.markdown(
    f"""
    <style>
    /* Force Markdown headers (H1) to the GOLD color */
    h1, h2{{
        color: {GOLD_COLOR} !important;
    }}
    h3{{
        color: {SECONDARY_GOLD_COLOUR} !important;
    }}
    
    /* FIX: Target the sidebar container and set the text color */
    [data-testid="stSidebar"] {{
        /* This applies to the elements inside the sidebar */
        color: {GOLD_COLOR} !important;
    }}
    
    /* Optional: Ensure all text elements (labels, markdown) within the sidebar use the color */
    [data-testid="stSidebar"] * {{
        color: {GOLD_COLOR} !important;
    }}
    
    /* NEW: Hide the judge_details.py link from the sidebar navigation */
    /* Streamlit converts pages/judge_details.py to the URL path /judge_details */
    [data-testid="stSidebarNavLink"][href$="/judge_details"] {{
        display: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- END CSS INJECTION ---

# Page Config
st.set_page_config(page_title="Search Court Hearings", layout="wide")

st.title("Search Through Court Hearings")
st.markdown("Use the filters below to explore recent hearings \
            stored in the Court Transcripts database.")

conn = get_db_connection()
data = get_data_from_db(conn)

# Ensure consistent date formats
data["hearing_date"] = pd.to_datetime(data["hearing_date"], errors="coerce")

# Sidebar / top Filters
col1, col2, col3, col4 = st.columns([2, 2, 2, 2])

with col1:
    keyword = st.text_input("Keyword Filter", \
                            placeholder="Enter keyword in title or description...")

with col2:
    court_filter = st.selectbox(
        "Court Filter",
        options=["All"] + sorted(data["court_name"].dropna().unique().tolist())
    )

with col3:
    # Handle empty data
    if data["hearing_date"].dropna().empty:
        default_start = default_end = datetime.date.today()
    else:
        default_start = data["hearing_date"].min().date()
        default_end = data["hearing_date"].max().date()

    # Provide single date if start==end, else tuple for range
    default_value = default_start if default_start == default_end else (default_start, default_end)

    date_selection = st.date_input(
        "Date Range",
        value=default_value
    )

    # Normalise to start_date and end_date
    if isinstance(date_selection, (tuple, list)):
        start_date, end_date = date_selection
    else:
        start_date = end_date = date_selection

with col4:
    ruling_filter = st.selectbox(
        "Ruling Favour",
        options=["All"] + sorted(data["judgement_favour"].fillna("Undisclosed").unique().tolist())
    )

filtered = data.copy()

# Keyword filter
if keyword:
    keyword_lower = keyword.lower()
    filtered = filtered[
        filtered["hearing_title"].str.lower().str.contains(keyword_lower, na=False)
        | filtered["hearing_description"].str.lower().str.contains(keyword_lower, na=False)
    ]

# Court filter
if court_filter != "All":
    filtered = filtered[filtered["court_name"] == court_filter]

# Ruling filter
if ruling_filter != "All":
    filtered = filtered[filtered["judgement_favour"].fillna("Undisclosed") == ruling_filter]

# Date range filter
if isinstance(start_date, datetime.date) and isinstance(end_date, datetime.date):
    if not filtered.empty:
        filtered = filtered[
            (filtered["hearing_date"].dt.date >= start_date)
            & (filtered["hearing_date"].dt.date <= end_date)
        ]

# Display
st.markdown(f"### Showing {len(filtered)} matching hearing(s)")

if filtered.empty:
    st.info("No hearings found matching your filters.")
else:
    for _, row in filtered.iterrows():
        ruling = row["judgement_favour"] or "Undisclosed"
        color = {
            "Plaintiff": "#AC8B13",
            "Defendant": "#00B5B8",
            "Undisclosed": "#6b7280"
        }.get(ruling, "#6b7280")

        with st.container():
            # Card layout
            st.subheader(row['hearing_title'] or "Untitled Hearing")
            st.caption(
                f"Court: {row['court_name'] or 'Unknown'} | "
                f"Date: {row['hearing_date'].date() if pd.notna(row['hearing_date']) else 'Unknown'} | "
                f"Citation: {row['hearing_citation'] or 'N/A'}"
            )
            st.write(row['hearing_description'] or "No description available.")

            # ruling badge
            st.markdown(
                f"<span style='background-color:{color}; color:white; padding:4px 10px; border-radius:6px; font-weight:500;'>{ruling}</span>",
                unsafe_allow_html=True
            )

            if row.get('hearing_url'):
                st.markdown(f"[🔗 View Full Hearing]({row['hearing_url']})")

            st.divider()  # separator between cards
