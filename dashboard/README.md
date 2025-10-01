# Dashboard

This folder contains all the python scripts used to create and run the Courts Transcripts Dashboard, as well as a helper `build_push_dockerfile.sh` to build and upload the image to AWS ECR.

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