"""Entry dashboard page"""

import logging
import streamlit as st
from dotenv import load_dotenv
from utils import setup_logging

load_dotenv()
setup_logging()

logging.info("Running dashboard.")
st.title('Court Transcript Dashboard')

col1, col2, col3 = st.columns(3)

with col1:
    # Placeholder until RDS is live
    st.metric("Total Court Hearings", 100, border=True)
