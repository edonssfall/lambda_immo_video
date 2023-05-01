from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import subprocess
import json


class YouTubeUploader:
    def __init__(self, client_secrets_file, scopes):
        self.client_secrets_file = client_secrets_file
        self.scopes = scopes
        self.youtube = None
        self.credentials = None
        self.metadata = None
        self.get_authenticated_service()

    def get_authenticated_service(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.client_secrets_file, self.scopes)
        self.credentials = flow.run_local_server(port=0)
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def get_video_metadata(self, video_path):
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        output = result.stdout.decode()
        self.metadata = json.loads(output)

    def upload_video(self, video_path, title, description, tags):
        try:
            media_file = MediaFileUpload(video_path)

            video = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags
                },
                'status': {
                    'privacyStatus': 'public'
                }
            }

            response = self.youtube.videos().insert(
                part='snippet,status',
                body=self.metadata,
                media_body=media_file
            ).execute()
            print(f"Video was successfully uploaded: {response['snippet']['title']}")
            return response
        except HttpError as error:
            print(f'An error occurred while uploading the video: {error}')
            return None
