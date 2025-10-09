from os import environ as ENV
import boto3
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def verify_email_identity():
    """Sends an email to the given Email Address to verify for SES email sending."""
    ses_client = boto3.client("ses",
                              aws_access_key_id=ENV['ACCESS_KEY'],
                              aws_secret_access_key=ENV['SECRET_KEY'],
                              region_name=ENV['REGION'])
    response = ses_client.verify_email_identity(
        EmailAddress=ENV['ORIGIN_EMAIL']

    )
    status_code = response['ResponseMetadata']['HTTPStatusCode']
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        ses_client.close()
        raise ConnectionError(f"{status_code}: Failed to send email.")
    logging.info('Verification email sent. Please verify before continuing.')


if __name__ == "__main__":
    load_dotenv()
    verify_email_identity()
