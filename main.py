import os
import urllib.request
import boto3
from dotenv import load_dotenv
from YoutubeUploader import YouTubeUploader

load_dotenv()

sqs = boto3.client('sqs')
queue_url = os.environ['QUEUE_URL']
project_dir = os.environ['WORK_DIRECTORY']
client_secrets_file = os.environ['CLIENT_SECRETS_FILE']
scopes = ['https://www.googleapis.com/auth/youtube.upload']



def lambda_handler(event, context):
    video_url = event['video_url']
    video_path = f'{project_dir}tmp/{os.path.basename(video_url)}'
    urllib.request.urlretrieve(video_url, video_path)

    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=event['receipt_handle'])

    uploader = YouTubeUploader(client_secrets_file, scopes)
    uploader.get_video_metadata(video_path)
    return uploader.upload_video(video_path, 'title', 'description', ['tags'])
