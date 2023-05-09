import boto3
import os
from dotenv import load_dotenv

load_dotenv()


class SQSProcessor:
    def __init__(self, queue_url):
        self.sqs = boto3.client('sqs')
        self.queue_url = queue_url

    def receive_message(self):
        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )
        messages = response.get('Messages', [])
        if messages:
            message = messages[0]
            receipt_handle = message['ReceiptHandle']
            return message, receipt_handle
        return None, None

    def delete_message(self, receipt_handle):
        self.sqs.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle
        )

    def send_message(self, message_body):
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=message_body
        )
