from unittest import TestCase
from unittest.mock import MagicMock, patch

from aws.SQSProcessor import SQSProcessor


class TestSQSProcessor(TestCase):
    def setUp(self) -> None:
        self.queue_url = 'https://example.com/queue'
        self.sqs = MagicMock()
        self.sqs_processor = SQSProcessor(self.queue_url)
        self.sqs_processor.sqs = self.sqs

    def test_receive_message_with_messages(self):
        self.sqs.receive_message.return_value = {
            'Messages': [{'MessageId': '123', 'Body': 'Test Message', 'ReceiptHandle': 'abc123'}]
        }
        message, receipt_handle = self.sqs_processor.receive_message()
        self.assertEqual(message['MessageId'], '123')
        self.assertEqual(message['Body'], 'Test Message')
        self.assertEqual(receipt_handle, 'abc123')

    def test_receive_message_without_messages(self):
        self.sqs.receive_message.return_value = {}
        message, receipt_handle = self.sqs_processor.receive_message()
        self.assertIsNone(message)
        self.assertIsNone(receipt_handle)

    def test_delete_message(self):
        self.sqs_processor.delete_message('123')
        self.sqs.delete_message.assert_called_with(
            QueueUrl=self.queue_url,
            ReceiptHandle='123'
        )

    def test_send_message(self):
        self.sqs_processor.send_message('Test Message')
        self.sqs.send_message.assert_called_with(
            QueueUrl=self.queue_url,
            MessageBody='Test Message'
        )