#pylint:disable=import-error
"""Streamlit page for showing further insights into judges. """
import datetime
import streamlit as st
import pandas as pd
from data_cache import get_data_from_db
from rds_utils import get_db_connection
from charts import get_judge_ruling_bias_chart, get_overall_ruling_bias_chart

PAGE_FILENAME = "judge_details"

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


st.set_page_config(page_title="Judge Details", layout="wide")

if st.button("⬅ Back to Search Judges"):
    # Use the filename (without extension) of the target page
    st.switch_page("pages/search_judges.py")

if "selected_judge_id" not in st.session_state:
    st.error("No judge selected. Please return to the Search Judges page.")
    st.stop()

judge_id = st.session_state["selected_judge_id"]

conn = get_db_connection()
data = get_data_from_db(conn)

judge_hearings = data[data["judge_id"] == judge_id].copy()

if judge_hearings.empty:
    st.warning("No hearing data found for this judge.")
    st.stop()

judge = judge_hearings.iloc[0]
FULL_NAME = " ".join(
    filter(None, [judge.get("title_name"), judge.get("first_name"), \
                  judge.get("middle_name"), judge.get("last_name")])
).strip()
appointment_date = judge.get("appointment_date", "Unknown")
court_name = judge.get("court_name", "Unknown")

judge_hearings["hearing_date"] = pd.to_datetime(judge_hearings["hearing_date"], errors="coerce")

total_cases = len(judge_hearings)
today = datetime.date.today()

month_str = today.strftime("%Y-%m")
month_cases = judge_hearings[judge_hearings\
                             ["hearing_date"].dt.to_period("M").astype(str) == month_str].shape[0]
year_cases = judge_hearings[judge_hearings["hearing_date"].dt.year == today.year].shape[0]

st.title(FULL_NAME or "Unknown Judge")
st.caption(f"{judge.get('title_name', 'Unknown Title')} | {court_name}")
st.markdown(f"**Appointed:** {appointment_date}")

col1, col2, col3 = st.columns(3)
col1.metric("Total Cases Seated", total_cases)
col2.metric("Cases This Month", month_cases)
col3.metric("Cases This Year", year_cases)

st.divider()

st.subheader("Ruling Bias Overview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Judge’s Ruling Bias**")
    bias_chart = get_judge_ruling_bias_chart(judge_hearings, FULL_NAME)
    st.altair_chart(bias_chart, use_container_width=True)

with col2:
    st.markdown("**Overall Ruling Bias (All Hearings)**")
    overall_chart = get_overall_ruling_bias_chart(data)
    st.altair_chart(overall_chart, use_container_width=True)

st.divider()

st.subheader("Most Recent Hearings")

recent = judge_hearings.sort_values("hearing_date", ascending=False).head(5)

for _, row in recent.iterrows():
    with st.container():
        st.markdown(f"### {row['hearing_title'] or 'Untitled Hearing'}")
        st.caption(
            f"Court: {row['court_name'] or 'Unknown'} | "
            f"Date: {row['hearing_date'].date() if pd.notna(row['hearing_date']) else 'Unknown'} | "
            f"Citation: {row['hearing_citation'] or 'N/A'}"
        )
        st.write(row.get("hearing_description") or "_No description available._")
        if row.get("hearing_url"):
            st.markdown(f"[View Full Hearing]({row['hearing_url']})")
        st.divider()
