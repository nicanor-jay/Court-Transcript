"""Script to scrape data from a website."""
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')  # Store your OpenAI key in a .env file
