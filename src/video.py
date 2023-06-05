import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        try:
            results = youtube.videos().list(part='snippet, statistics', id=self.video_id).execute()['items']
            if results:
                video = results[0]['snippet']
                self.title = video['title']
                self.url = f'https://www.youtube.com/watch?v={self.video_id}'
                self.view_count = int(
                    youtube.videos().list(part='statistics', id=self.video_id).execute()['items'][0]['statistics'][
                        'viewCount'])
                self.like_count = int(
                    youtube.videos().list(part='statistics', id=self.video_id).execute()['items'][0]['statistics'][
                        'likeCount'])
            else:
                self.title = None
                self.url = None
                self.view_count = None
                self.like_count = None
        except HttpError:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        super().get_service()
        self.playlist_id = playlist_id
        self.video_id = video_id
        self.video_info = self.get_service().videos().list(
            part='snippet, statistics', id=self.video_id).execute()['items'][0]['snippet']
        self.title = self.video_info['title']
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.view_count = int(self.get_service().videos().list(
            part='snippet, statistics', id=self.video_id).execute()['items'][0]['statistics']['viewCount'])
        self.like_count = int(self.get_service().videos().list(
            part='snippet, statistics', id=self.video_id).execute()['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return self.title
