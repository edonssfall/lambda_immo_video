import os
import urllib.request
from dotenv import load_dotenv
from youtube.YouTubeUploader import YouTubeUploader
from aws.SQSProcessor import SQSProcessor

load_dotenv()

project_dir = os.environ['WORK_DIRECTORY']
client_secrets_file = os.environ['CLIENT_SECRETS_FILE']
scopes = ['https://www.googleapis.com/auth/youtube.upload']

queue_url_standard = os.environ['QUEUE_URL_STANDARD']
queue_arn_standard = os.environ['QUEUE_ARN_STANDARD']
queue_url_fifo = os.environ['QUEUE_URL_FIFO']
queue_arn_fifo = os.environ['QUEUE_ARN_FIFO']


def lambda_handler(event, context):
    sqs = SQSProcessor(event['queue_url'])

    video_url = sqs.receive_message()
    video_path = f'{project_dir}tmp/{os.path.basename(video_url)}'
    urllib.request.urlretrieve(video_url, video_path)

    uploader = YouTubeUploader(client_secrets_file, scopes)
    uploader.get_video_metadata(video_path)
    video_youtube_url = uploader.upload_video(video_path, 'title', 'description', ['tags'])

    receipt_handle = event['Records'][0]['receiptHandle']
    sqs.delete_message(receipt_handle=receipt_handle)
    return sqs.send_message(message_body=video_youtube_url)
