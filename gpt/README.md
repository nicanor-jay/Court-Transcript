# Contents
1. [`summary.py`](#summarypy)

## `summary.py`

A script designed to make requests to the GPT-API to retrieve the necessary data for the Court Transcript ETL pipeline. This data includes:

**- meaningful headers:** headers from a court transcript that the ai deems meaningful enough to use it's corresponding text to summarise the transcript

**- transcript summaries:** summary of a text from a court transcript (based on the useful headers) returning the following information:
```
{
    "summary": [a concise description of what the hearing was about, maximum 1000 characters],
    "ruling": [which party the court ruled in favour of (one word answer e.g. Defendant)],
    "anomaly": [whether anything irregular happened in the context of a normal court hearing]
}
```

The meaningful headers request should be used to generate the transcript summaries.

### Usage

This script is intended to be imported as a module by other scripts (it has no "standalone" functionality). To use this script, simply import it as:

```python
""" Your module. """

from summary import extract_meaningful_headers, summarise
```

The `extract_meaningful_headers` method will take a *list of dicts, may change once webscraping functionality implemented* and return a `{identifier:[headers]}` dictionary where:
- `identifier` is the unique identifier for a specific court transcript
- `[headers]` is a list of all the meaningful headers from the transcript

The `summarise` method will take a *list of dicts, may change once webscraping functionality implemented* and return a `{identifier: {transcript_summary}}` dictionary where:
- `identifier` is the unique identifier for a specific court transcript
- `{transcript_summary}` is a dictionary storing the summary data which will be in the form:
```
{
    "summary": [a concise description of what the hearing was about, maximum 1000 characters],
    "ruling": [which party the court ruled in favour of (one word answer e.g. Defendant)],
    "anomaly": [whether anything irregular happened in the context of a normal court hearing]
}
```

Make sure you have a .env file containing your openai api key for the script to run.

```
OPENAI_API_KEY=
```