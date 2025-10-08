#pylint:disable=import-error
"""Script to search for specific judges within the DB via keyword filers etc. """
import streamlit as st
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

st.set_page_config(page_title="Search Judges", layout="wide")

st.title("Search Judges")
st.markdown("Use the filters below to explore judges in the Court Transcripts database.")

# Load hearing data
conn = get_db_connection()
data = get_data_from_db(conn)

# Extract unique judges
judges_df = data[["judge_id", "first_name", \
                  "middle_name", "last_name", "title_name", "court_name"]].drop_duplicates()

# Combine names
judges_df["name"] = (
    judges_df["title_name"].fillna("") + " " +
    judges_df["first_name"].fillna("") + " " +
    judges_df["middle_name"].fillna("") + " " +
    judges_df["last_name"].fillna("")
).str.replace(r"\s+", " ", regex=True).str.strip()

# Keep only necessary columns
judges_df = judges_df[["judge_id", "name", "title_name", "court_name"]].rename(
    columns={"judge_id": "id", "title_name": "title"}
)

# Fill missing values
judges_df["name"] = judges_df["name"].fillna("Unknown")
judges_df["title"] = judges_df["title"].fillna("Unknown")
judges_df["court_name"] = judges_df["court_name"].fillna("Unknown")

# Filters
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    name_filter = st.text_input("Judge Name", placeholder="Enter judge name...")
with col2:
    title_filter = st.selectbox("Judge Title", \
                                ["All"] + sorted(judges_df["title"].unique().tolist()))
with col3:
    court_filter = st.selectbox("Court", ["All"] + \
                                sorted(judges_df["court_name"].unique().tolist()))

# Apply filters
filtered = judges_df.copy()
if name_filter:
    name_lower = name_filter.lower()
    filtered = filtered[filtered["name"].str.lower().str.contains(name_lower, na=False)]
if title_filter != "All":
    filtered = filtered[filtered["title"] == title_filter]
if court_filter != "All":
    filtered = filtered[filtered["court_name"] == court_filter]

filtered = filtered.drop_duplicates(subset="id").reset_index(drop=True)

# Display results
st.markdown(f"### Showing {len(filtered)} matching judge(s)")

if filtered.empty:
    st.info("No judges found matching your filters.")
else:
    for idx, row in filtered.iterrows():
        with st.container():
            cols = st.columns([4, 1])
            with cols[0]:
                st.subheader(row["name"])
                st.caption(f"{row['title']} | {row['court_name']}")
            with cols[1]:
                if st.button("View Details", key=f"judge_{row.id}_{idx}"):
                    st.session_state["selected_judge_id"] = row["id"]
                    st.switch_page("pages/judge_details.py")
