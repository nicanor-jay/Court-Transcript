# UK Case Law ETL Pipeline


A Python ETL pipeline that extracts both judge information from the UK Judiciary website ([judiciary.uk](https://www.judiciary.uk)) and
court hearings from the Case Law National Archive Website ([caselaw.gov.uk](https://caselaw.nationalarchives.gov.uk/)), extracts the meaningful information from the court transcript, and also summarises the contents of the document with GPT-API. Valid data is then uploaded to the RDS for usage in the dashboard & associated services.

## Features

- Scrapes judges
- Downloads a (variable) amount of recent XML files
- Cleans & Transforms the data with Python & GPT-API
  - Names & titles extracted from new judges
  - Hearing details summaries by GPT-API
- Uploads new judges & court hearings to the RDS

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository

2. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install [Playwright](https://playwright.dev) browsers:
```bash
playwright install chromium
```

## Usage

### Running the Scraper


From the root directory, run
```bash
python -m pipeline.etl
```

This will:
1. Create `headers_input.json` with all subtitles for each court hearing. Given to GPT-API to retrieve meaningful headers.
2. Create `summary_input.json` with all meaningful subtitles & texts for each court hearing. Given to the GPT-API for summarisation.