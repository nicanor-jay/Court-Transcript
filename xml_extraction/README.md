# Contents
1. [`parse_xml.py`](#parse_xmlpy)
2. [`metadata_xml.py`](#metadata_xmlpy)

## `parse_xml.py`

A script that is designed to _roughly_ detect headings within a XML court transcript from the [National Archives](https://caselaw.nationalarchives.gov.uk/) and its corresponding text.

### Usage

This script is intended to be imported as a module by other scripts (it has no "standalone" functionality). To use this script, simply import it as:

```python
""" Your module. """

from parse_xml import get_label_text_dict

...
```

This method will take a filepath to an `.xml` file, and return a `{label:text}` dictionary where:
- `label` is the heading text
- `text` is the raw text under that heading

Note that two special headings may be added - `DOC_START` and `DOC_END` - for raw text which does not have a heading at the head/tail of the XML file.

## `metadata_xml.py`

A script which will extract metadata contained in a XML court transcript from the [National Archives](https://caselaw.nationalarchives.gov.uk/).

### Usage

This script is intended to be imported as a module by other scripts - however, it can also be used standalone.

#### As a module

For use as a module, import like so:

```python
""" Your module. """

from metadata_xml import get_metadata

...
```

`get_metadata()` takes a raw XML file string, and returns a dictionary containing metadata about that file.

Specifically, the data returned is:
- `title` (`str`): The title of the hearing.
- `citation` (`str`): Neutral citation; can be used as unique identifier.
- `verdict_date` (`datetime`): The date when judgement was handed down.
- `court` (`str`): The name of the court where the hearing took place.
- `url` (`str`): A URL to the hearing transcript page.
- `judges` (`list[str]`): A list containing the names of judges who sat the hearing.

> **NOTE**:
>
> If a _field of metadata_ is not found, then it will be |**returned as `None`**.
>
> If the XML file is _missing a `<meta>` element entirely_, the script **will raise a `KeyError`**.

#### As a script

For use as a script, you must call the script like so:

```bash
$ python metadata_xml.py -f <filename.xml>
```

The script accepts two CLI arguments:

- `-f`: path to XML file to extract from; mandatory.
- `-o`: output data to JSON file.

You can also call the script with `-h` to view a summary of the arguments listed above.

## `get_unique_xml.py`

This script - using `metadata_xml.py` and `case_fetcher.py` - will return, up to the last 20, **most recent and unique** XML hearing transcripts as string objects.

### Usage

This script is intended to be imported as a module by other scripts (it has no "standalone" functionality). To use this script, simply import it as:

```python
""" Your module. """

from get_unique_xml import get_unique_xmls

...
```

`get_unique_xmls()` will return a list of XML strings that are guaranteed to be unique against the PostgreSQL service that is defined inside your `.env` (see the README.md in the root directory for more details).