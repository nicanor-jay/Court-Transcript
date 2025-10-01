"""Entry dashboard page"""

import logging
import streamlit as st
from dotenv import load_dotenv
from utils import setup_logging

load_dotenv()
setup_logging()

logging.info("Running dashboard.")
st.title('Court Transcript Dashboard')
