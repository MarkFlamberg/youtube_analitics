import os
from googleapiclient.discovery import build
import json


class Video:

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        self.video_info = self.get_service().videos().list(
            part='snippet, statistics', id=self.video_id).execute()['items'][0]['snippet']
        self.title = self.video_info['title']
        self.url = f'https://www.youtube.com/watch?v={self.video_id}'
        self.video_count = int(self.get_service().videos().list(
            part='snippet, statistics', id=self.video_id).execute()['items'][0]['statistics']['viewCount'])
        self.like_count =  int(self.get_service().videos().list(
            part='snippet, statistics', id=self.video_id).execute()['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return self.title

    def get_service(self):
        """Метод для работы с api"""

        api_key: str = os.getenv('YT_API_KEY')  # API_KEY скопирован из гугла и вставлен в переменные окружения
        service = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API
        return service


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
