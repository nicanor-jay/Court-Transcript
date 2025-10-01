# Contents
1. `parse_xml.py`

## `parse_xml.py`

A script that is designed to _roughly_ detect headings within a XML court transcript from the [National Archives](https://caselaw.nationalarchives.gov.uk/) and its corresponding text.

### Use

This script is intended to be imported as a module by other scripts (it has no "standalone" functionality). To use this script, simply import it as:

```python
""" Your module. """

from parse_xml.py import get_label_text_dict

...
```

This method will take a filepath to an `.xml` file, and return a `{label:text}` dictionary where:
- `label` is the heading text
- `text` is the raw text under that heading

Note that two special headings may be added - `DOC_START` and `DOC_END` - for raw text which does not have a heading at the head/tail of the XML file.