# pylint: skip-file

"""Very hacky way of accessing case_fetcher.py from here."""

import sys
from os.path import abspath, isdir

# insert case_fetcher dir into Python path
# this lets us import case_fetcher.py
case_fetcher_path = abspath("../case_fetcher")
if not isdir(case_fetcher_path):
    case_fetcher_path = abspath("case_fetcher")

sys.path.append(case_fetcher_path)

from case_fetcher import fetch_feed, get_xml_entries, load_all_xml
