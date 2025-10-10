## API

### Contents
1. [Running locally](#running-the-api-locally)
2. [As a Docker container](#running-as-a-docker-container)
3. [Pushing to an ECR](#pushing-to-an-aws-ecr)

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
ECR_FOR_API_NAME=
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

### Running as a Docker container

You can run this API as a Docker container. To do so, first build the image:

```bash
$ docker buildx build . -t "$ECR_FOR_API_NAME":latest
```

You can then run it locally with:

```bash
$ docker run --env-file .env -p 5000:5000 "$ECR_FOR_API_NAME":latest
```

### Pushing to an AWS ECR

You can easily push to an AWS ECR instance by running:

```bash
$ bash build_push_dockerfile.sh
```