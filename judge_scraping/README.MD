# UK Judiciary Web Scraper

A Python web scraper that extracts judge information from the UK Judiciary website ([judiciary.uk](https://www.judiciary.uk)) and outputs structured JSON data.

## Features

- Scrapes judge names, titles, and appointment dates
- Handles complex name parsing (multi-word surnames, post-nominals)
- Supports surname prefixes (van der, de la, von, etc.)
- Removes post-nominal titles (KC, QC, CBE, etc.)
- Extracts and normalises judicial titles
- Outputs normalised data ready for database import
- Comprehensive test suite included

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

```bash
python judge_scraping.py
```

This will:
1. Scrape all judge data from [judiciary.uk](https://www.judiciary.uk)
2. Create `judges_data.json` with all judge records
3. Create `titles_data.json` with normalised title data

### Output Files

**`judges_data.json`** - Contains individual judge records:
```json
[
  {
    "source_url": "https://www.judiciary.uk/...",
    "full_name": "His Honour Judge Anthony Dennis Watson KC",
    "title": "His Honour Judge",
    "title_id": 5,
    "first_name": "Anthony",
    "middle_name": "Dennis",
    "last_name": "Watson",
    "appointment_date": "2012-07-09"
  }
]
```

**`titles_data.json`** - Contains normalised title data:
```json
[
  {
    "title_id": 1,
    "title_name": "District Judge"
  },
  {
    "title_id": 2,
    "title_name": "His Honour Judge"
  }
]
```

### Scraping into RDS

```bash
python3 judges_rds.py
```

This will:
1. Run the scraper as above
2. Iterate through all scraped judges
   1. Gets / Inserts the title from / into the RDS
   2. Inserts the Judge into the RDS. Postgres & the schema set-up will handle any duplicates automatically.

## Running Tests

Run the complete test suite:
```bash
pytest test_judge_scraping.py -v
```

Run specific test classes:
```bash
pytest test_judge_scraping.py::TestParseName -v
```

Run with coverage report:
```bash
pip install pytest-cov
pytest test_judge_scraping.py --cov=judge_scraping --cov-report=html
```

## Name Parsing Features

### Supported Titles
- District Judge (MC), District Judge
- Lord/Lady Justice
- His/Her Honour Judge
- Sir, Dame, Lord, Lady
- Mr, Mrs, Miss, Ms
- Dr, Professor
- Judge, HHJ, DHJ

### Post-Nominal Handling
Automatically removes post-nominal titles:
- KC, QC (King's/Queen's Counsel)
- CBE, OBE, MBE (Honours)
- JP (Justice of the Peace)

### Surname Prefix Support
Correctly handles multi-word surnames with prefixes:
- van, van der, van den
- de, de la
- du
- von, von der

**Examples:**
- "Judge van der Zwart" → last_name: "van der Zwart"
- "Judge John van den Berg" → first: "John", last: "van den Berg"
- "Sir Anthony Watson KC" → first: "Anthony", last: "Watson" (KC removed)

## Project Structure

```
.
├── judge_scraping.py          # Main scraper script
├── test_judge_scraping.py     # Test suite
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── judges_data.json          # Output: judge records (generated but gitignored)
└── titles_data.json          # Output: title records (generated but gitignored)
```

## Database Integration

The output JSON files are structured for easy import into a relational database:

### Suggested Schema

```sql
CREATE TABLE title (
    title_id BIGINT PRIMARY KEY,
    title_name VARCHAR(255)
);

CREATE TABLE judge (
    judge_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title_id BIGINT,
    first_name VARCHAR(255),
    middle_name VARCHAR(255),
    last_name VARCHAR(255),
    appointment_date TIMESTAMP,
    FOREIGN KEY (title_id) REFERENCES title(title_id)
);
```

## Troubleshooting

### Playwright Installation Issues
If you encounter browser installation issues:
```bash
playwright install-deps  # Install system dependencies
playwright install chromium
```

### Timeout Errors
If scraping times out, increase the timeout in the code:
```python
page.goto(url, wait_until="domcontentloaded", timeout=30000)  # 30 seconds
```

### Missing Data
Some judges may not have appointment dates or complete name information. The scraper handles this gracefully by setting fields to `None`.

## Contributing

To add support for new name patterns:

1. Add the pattern to the appropriate list (`TITLES`, `POST_NOMINALS`, or `SURNAME_PREFIXES`)
2. Add test cases to `test_judge_scraping.py`
3. Run tests to ensure no regressions: `pytest test_judge_scraping.py -v`

## Notes

- The scraper respects the [judiciary.uk](https://www.judiciary.uk) website structure
- Website structure changes may require updates to the scraper
- Always review scraped data for accuracy before use
- Consider rate limiting if running frequent scrapes

## Support

For issues or questions:
1. Check the test suite for expected behavior examples
2. Review the inline code documentation
3. Verify your Python and dependency versions match requirements