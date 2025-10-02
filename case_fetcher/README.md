# UK Caselaw XML Fetcher

A Python utility to fetch recent legal case entries from the UK National Archives Caselaw website's Atom feed, extract links to the Akoma Ntoso XML files, and optionally download them to a local directory.

The script connects to the Caselaw Atom feed, parses the entries, and fetches the corresponding full XML documents for storage or further processing.

---

## Features

* Fetches case entries from the official National Archives Caselaw Atom feed.
* Extracts the Akoma Ntoso XML link for each case.
* Supports fetching a custom number of cases per page.
* Safely downloads XML files, using a slugified case title as the filename.
* Includes a utility function (`slugify`) for creating safe, 100-character-limited filenames.
* Comprehensive test suite included using `pytest` and `responses` for mocking HTTP requests.

---

## Installation

### Prerequisites

* Python 3.9 or higher
* `pip` (Python package manager)

### Setup

1. Clone or download this repository (or place the files in a project directory).
2. Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Running the Fetcher

The script fetches the case feed, loads the XMLs into memory, and optionally saves them to a local folder named `xml_cases`.

```bash
python case_fetcher.py [options]
```

### Options

| Argument     | Type | Default | Description                                            |
| ------------ | ---- | ------- | ------------------------------------------------------ |
| `--per-page` | int  | 10      | Number of cases to fetch from the Atom feed.           |
| `--download` | flag | N/A     | If set, the fetched XMLs will be saved to `xml_cases`. |

### Examples

1. Fetch 10 cases into memory (default):

```bash
python case_fetcher.py
```

*Output will show how many XMLs were loaded, but files will not be saved.*

2. Fetch 25 cases and save XML files:

```bash
python case_fetcher.py --per-page 25 --download
```

*XML files will be saved in the `xml_cases` directory.*

---

## Output Directory

By default, files are saved to the relative directory `xml_cases`.

```
.
└── xml_cases/
    ├── Sample_Case_v_Another_Case__2024__UKSC_1.xml
    └── Test_Case__2024__EWCA_100.xml
```

---

## Running Tests

The test suite uses `pytest` and `responses` to mock all external HTTP calls, ensuring tests are fast and reliable.

* Run the complete test suite:

```bash
pytest test_case_fetcher.py -v
```
---

## Project Structure

```
.
├── case_fetcher.py            # Main fetching and downloading logic
├── test_case_fetcher.py       # Comprehensive test suite (using pytest and responses)
├── requirements.txt           # Python dependencies (requests, pytest, etc.)
└── README.md                  # This file
```

---

## Troubleshooting

### HTTP/Network Errors

The `fetch_feed` and `load_single_xml` functions will raise an exception if a non-200 HTTP status code is received.

* Check your network connection.
* Verify the `BASE_FEED_URL` in `case_fetcher.py` is correct.

### Filename Issues

The `slugify` function handles special characters and limits filenames to 100 characters to prevent filesystem errors.

```python
slugify("Case [2024] UKSC/1")  # → "Case_2024_UKSC_1"
```

### Missing XML Files

Some entries in the Atom feed may not include a link to the Akoma Ntoso XML file. These cases are skipped and a message is printed:

```
No XML for: No XML Case [2024] EWHC 50 (https://caselaw.nationalarchives.gov.uk/id/ewhc/2024/50)
```

---

## Support

For issues or questions, please check:

* The `test_case_fetcher.py` file for examples of expected function behavior.
* The docstrings in `case_fetcher.py` for function details.
* The dependencies listed in `requirements.txt`.
