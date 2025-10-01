# Court Transcript Pipeline

The National Archives release transcripts of real court hearings every day. They are given in plain text on the NA website.

These transcripts are released more frequently than a person could read them and are often hard to consume for the average person. Additionally, it is hard to search through this data so you can research further. For example

How many cases has a judge sat? 
How often do they rule one way or another?
Do specific judges have bias?
etc

Overall, the problem is that the public does not have sufficient access or knowledge of what happens inside courtrooms and the people who have traditionally solved this problem (journalists) are currently in massive decline because of wider market reasons. This tool can help the public to properly understand court judgements and also streamline the process of journalists communicating court proceedings with the public.

The solution? A data pipeline to automate the enhancement, discoverability and and analysis of real Courtroom documents.


# Deliverables
- Deployed pipeline, hosted in the cloud.
- Database solution storing the full data for court hearings & judges.
- Deployed dashboard website.


# Team
- **Architecture & DevOps**: riaz1751 & arbeh0
- **Quality Assurance**: lenaverse
- **Project Manager**: nicanor-jay & cameronriley0
- **Engineer & Analyst**: All of the above


## Requirements
1. A `.env` formatted as follows.
```ini
ACCESS_KEY={your_aws_key}
SECRET_ACCESS_KEY={your_aws_secret_key}
REGION={region}
S3_NAME={bucket_name}
DB_HOST={db_host}
DB_PORT={db_port}
DB_NAME={db_name}
DB_USERNAME={db_username}
DB_PASSWORD={db_password}

# Dashboard folder env vars for build_dockerfile.sh
AWS_ACCOUNT_ID={aws_account_id}
APP_NAME={app_name}
DASHBOARD_ECR_NAME={dashboard_ecr_name}
```

## Terraform Phases
### Phase One
Run `phase-one` module of the terraform steps to create the initial, non-dependant resources up on AWS.

### Phase Two

Phase Two is dependant on the following steps having been completed

- Pipeline container being uploaded to ECR.
- ECS Task container being uploaded to ECR.
- Dashboard container being uploaded to ECR. 

Once the above three steps are completed, you can run the `phase-two` module of the terraform steps.