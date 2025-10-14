"""This script sends emails with boto3 to the subscriber list."""

from os import environ as ENV
import boto3
import logging
from dotenv import load_dotenv
from create_email import get_subscribers_and_email

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def send_html_email(subscriber_list: list, email_html: str):
    """Sends the daily email to the subscribers."""
    ses_client = boto3.client("ses",
                              aws_access_key_id=ENV['ACCESS_KEY'],
                              aws_secret_access_key=ENV['SECRET_ACCESS_KEY'],
                              region_name=ENV['REGION'])
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "BccAddresses": subscriber_list,
        },
        Message={
            "Body": {
                "Html": {
                    "Charset": CHARSET,
                    "Data": email_html,
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": "Barrister Brief Daily Report",
            },
        },
        Source=ENV['ORIGIN_EMAIL'],
    )

    response_code = response['ResponseMetadata']['HTTPStatusCode']

    if response_code != 200:
        logging.error('Response code %s', )
    else:
        logging.info('Emails sent!')


def handler(event=None, context=None):
    """Handler entry point"""
    load_dotenv()

    if not ENV['ORIGIN_EMAIL']:
        logging.critical("Missing ORIGIN_EMAIL env var.")
        return

    if not ENV['DASHBOARD_URL']:
        logging.critical("Missing DASHBOARD_URL env var.")
        return

    subscribers_email_dict = get_subscribers_and_email(ENV['DASHBOARD_URL'])

    subscribers = subscribers_email_dict['subscriber_emails']
    email = subscribers_email_dict['email']
    num_hearings = subscribers_email_dict['num_hearings']

    if len(subscribers) < 1:
        logging.info("No subscribers found. Aborting")
        return

    if num_hearings < 1:
        logging.info("No hearings found. Aborting")
        return

    logging.info("Sending email to %s subscribers.", len(subscribers))
    send_html_email(subscribers, email)


if __name__ == "__main__":
    handler()
