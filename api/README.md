## API

This module contains code for an API service that exposes programmatic access to the Barrister Brief database.

In order to be able to properly use any part of this module, you must first have a `.env` file within this directory, with the following details/credentials:

```bash
ACCESS_KEY=
SECRET_ACCESS_KEY=
REGION=
AWS_ACCOUNT_ID=
DB_HOST=
DB_PORT=
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
```

### Running the API locally

To run the API locally, first create a virtual environment and activate it:
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Then install all requirements:
```bash
$ pip install -r requirements.txt
```

Lastly, run the API:

```bash
$ python api.py
```

This will run the API at `0.0.0.0` on port `5000`.