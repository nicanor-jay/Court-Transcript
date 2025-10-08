# Create Email scripts

A Python script intended to be used as a Lambda which takes yesterday's court hearings and current
subscriber list, formulates an email with HTML, then returns both as a dictionary to be used in a step
function.

## Features

- Downloads yesterdays court transcript hearings from the RDS
- Downloads all subscribers in the subscriber table
- Formulates a HTML email
- Returns the HTML email & subscriber list for usage in our step function as a dict. e.g.

```
{
    'subscriber_emails': ['email1', 'email2', 'email3'],
    'email': <HTML email string>
}

```


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
pip install -r requirements.txt
```

## Usage

### Running the script

From within the directory.
```bash
python create_email.py
```

## Containerising the email task

### Requirements

A `.env` file as described in the root level [README.md](../README.md)

### Usage

To containerise the pipeline and upload to ECR, run the following command from the root directory.

```bash
bash email/build_push_dockerfile.sh
```

This will build, tag, & upload the containerised image to AWS ECR.