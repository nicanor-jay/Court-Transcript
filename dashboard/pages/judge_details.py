#pylint:disable=import-error
"""Streamlit page for showing further insights into judges. """
import datetime
import streamlit as st
import pandas as pd
from data_cache import get_data_from_db, get_summaries_for_judge
from rds_utils import get_db_connection
from charts import (
    get_judge_ruling_tendency_chart,
    get_overall_ruling_tendency_chart,
    create_word_cloud
)

PAGE_FILENAME = "Judge_Details"

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
    [data-testid="stSidebarNavLink"][href$="/Judge_Details"] {{
        display: none;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- END CSS INJECTION ---

MAIN_LOGO = "images/BarristerBrief.png"
SIDEBAR_LOGO = "images/courtlogo.png"

st.logo(SIDEBAR_LOGO, size='large')
st.sidebar.image(MAIN_LOGO)

st.set_page_config(page_title="Judge Details", layout="wide")

if st.button("⬅ Back to Search Judges"):
    st.switch_page("pages/Search_Judges.py")

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

# STATISTICS PANEL
st.subheader("Judge Statistics")

# Calculate ruling favour breakdown
judge_hearings_copy = judge_hearings.copy()
judge_hearings_copy["judgement_favour"] = judge_hearings_copy["judgement_favour"].fillna("Undisclosed")
ruling_counts = judge_hearings_copy["judgement_favour"].value_counts().to_dict()

plaintiff_count = ruling_counts.get("Plaintiff", 0)
defendant_count = ruling_counts.get("Defendant", 0)
undisclosed_count = ruling_counts.get("Undisclosed", 0)

# Calculate percentages
plaintiff_pct = (plaintiff_count / total_cases * 100) if total_cases > 0 else 0
defendant_pct = (defendant_count / total_cases * 100) if total_cases > 0 else 0
undisclosed_pct = (undisclosed_count / total_cases * 100) if total_cases > 0 else 0

# Display metrics
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Cases", total_cases)

with stat_col2:
    st.metric("Plaintiff Favoured", f"{plaintiff_count} ({plaintiff_pct:.1f}%)")

with stat_col3:
    st.metric("Defendant Favoured", f"{defendant_count} ({defendant_pct:.1f}%)")

with stat_col4:
    st.metric("Undisclosed", f"{undisclosed_count} ({undisclosed_pct:.1f}%)")

# Most common courts
courts = judge_hearings_copy["court_name"].value_counts().head(5)

st.markdown("**Most Common Courts:**")
if not courts.empty:
    courts_text = ", ".join([f"{court} ({count})" for court, count in courts.items()])
    st.write(courts_text)
else:
    st.write("No court data available.")

st.divider()

st.subheader("Ruling Tendency Overview")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Judge's Ruling Tendency**")
    tendency_chart = get_judge_ruling_tendency_chart(judge_hearings, FULL_NAME)
    st.altair_chart(tendency_chart, use_container_width=True)

with col2:
    st.markdown("**Overall Ruling Tendency (All Hearings)**")
    overall_chart = get_overall_ruling_tendency_chart(data)
    st.altair_chart(overall_chart, use_container_width=True)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Judge's Case's Wordcloud")
    st.markdown("**Judge's Case Wordcloud**")
with col2:
    text_data = get_summaries_for_judge(conn, judge_id)
    judge_word_cloud = create_word_cloud(text_data)
    image = judge_word_cloud.to_image()
    st.image(image, use_container_width=1000)


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