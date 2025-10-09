"""
Streamlit dashboard layout for court hearings data.
"""

import streamlit as st
from dotenv import load_dotenv
from rds_utils import get_db_connection
from data_cache import (
    get_data_from_db,
)
from charts import (
    get_recent_hearings_table,
    get_rulings_by_court_chart,
    get_overall_ruling_tendency_chart,
    get_rulings_by_title,
    get_anomalies_visualisation
)

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

def main():
    """Main function to load and create dashboard. """
    load_dotenv()

    # Keeping layout="wide" as it is a layout setting, not a theme setting.
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
        st.altair_chart(get_overall_ruling_tendency_chart(data), use_container_width=True)

        st.markdown("### Recent Court Anomalies")
        st.altair_chart(get_anomalies_visualisation(data), use_container_width=True)


if __name__ == "__main__":
    main()
    