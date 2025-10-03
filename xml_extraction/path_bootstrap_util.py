"""Very hacky way of accessing case_fetcher.py from here."""

import sys

# insert case_fetcher dir into Python path
# this lets us import case_fetcher.py
sys.path.append("/Users/arshinbehjat/Documents/sigma-labs/Court-Transcript/case_fetcher")
from case_fetcher import fetch_feed, get_xml_entries, load_all_xml