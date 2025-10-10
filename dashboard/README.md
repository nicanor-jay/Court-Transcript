# Dashboard

This folder contains all the python scripts used to create and run the Courts Transcripts Dashboard, as well as a helper `build_push_dockerfile.sh` to build and upload the image to AWS ECR.

## Scripts
### `dashboard.py`
This script is the main entrypoint of the dashboard, and is what will give the Streamlit UI the structure and layout.

### `charts.py`
This file will hold all of the functions to create and return Altair charts which will be shown on the dashboard pages.

### `data_cache.py`
This script will hold all functions used to query the RDS which will return the output as Pandas DataFrames. The outputs of each function in this script will also be cached with the `@st.cache_data` decorator to improve efficiency.

### `rds_utils.py`
This RDS utility script holds all functions used to connect and send queries to the RDS.

### `utils.py`
This utility script holds helper functions, such as a function to setup the logging used for the dashboard code.

### `.streamlit/config.toml`
Holds the custom colour themes for the streamlit app

## Folders
### `pages/`
This folder holds the necessary scripts to run the sidebar and multi-page view 

### `images/`
This folder holds the necessary images for logos for the streamlit webpage

## Requirements
1. A root level `.env` file formatted as stated in the [project level readme](../README.md).


## Usage

### Locally
Run the dashboard locally with
```bash
streamlit run dashboard.py
```
### AWS Hosted

Provided that you have filled out the project level `.env` file as specified, you can also make use of `build_push_dockerfile.sh` by

```bash
bash build_push_dockerfile.sh
```

Which automatically builds and pushes your dashboard image up to the specified ECR Repository on AWS.

Once the image is hosted on the ECR Repository, and you have completed all other steps for terraform stage two, running the stage two instructions will create a task definition for the dashboard, as well as begin hosting it as an ECS Fargate Service.