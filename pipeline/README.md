# UK Case Law ETL Pipeline


A Python ETL pipeline that extracts both judge information from the UK Judiciary website ([judiciary.uk](https://www.judiciary.uk)) and
court hearings from the Case Law National Archive Website ([caselaw.gov.uk](https://caselaw.nationalarchives.gov.uk/)), extracts the meaningful information from the court transcript, and also summarises the contents of the document with GPT-API. 

Valid data is then uploaded to the RDS for usage in the dashboard & associated services.

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

The following command finds all requirements in the project and installs them.
```bash
find . -type f -name "requirements.txt" | sed -e 's/^/-r /' | xargs pip install
```

## Usage

### Running the Scraper


From the root directory, run
```bash
python -m pipeline.etl
```

You can also use the CLI argument of `-n`/`--number` to denote how many XML's you want to download (defaulted to 20)

```bash
python -m pipeline.etl -n 10
```

This will:
1. Create `headers_input.json` with all subtitles for each court hearing. Given to GPT-API to retrieve meaningful headers.
2. Create `summary_input.json` with all meaningful subtitles & texts for each court hearing. Given to the GPT-API for summarisation.

## Containerising the Pipeline

### Requirements

A `.env` file as described in the root level [README.md](../README.md)

### Usage

To containerise the pipeline and upload to ECR, run the following command from the root directory.

```bash
bash pipeline/build_push_dockerfile.sh
```

This will build, tag, & upload the containerised image to AWS ECR.