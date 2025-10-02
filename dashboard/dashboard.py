"""Entry dashboard page"""

import logging
import streamlit as st
from dotenv import load_dotenv
from utils import setup_logging
from rds_utils import get_db_connection
from data_cache import get_total_hearing_count

con = get_db_connection()
load_dotenv()
setup_logging()

logging.info("Running dashboard.")
st.title('Court Transcript Dashboard')

col1, col2, col3 = st.columns(3)


with col1:
    # Placeholder until RDS is live
    st.metric("(Fake) Total Court Hearings", 100, border=True)
with col2:
    st.metric("(RDS) Total Court Hearings",
              get_total_hearing_count(con)['total'], border=True)
