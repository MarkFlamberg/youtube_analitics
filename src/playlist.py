import datetime
import isodate
import os
from googleapiclient.discovery import build


class PlayList():

    def __init__(self, playlist_id):
        api_key: str = os.getenv('API_KEY')  # API_KEY скопирован из гугла и вставлен в переменные окружения
        youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

        self.playlist_id = playlist_id
        self.playlist_info = youtube.playlists().list(part="snippet", id=self.playlist_id).execute()['items'][0][
            'snippet']  # Информация о плейлисте
        self.title = self.playlist_info['title']  # Название плейлиста
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'  # Сылка на плейлист
        self.playlist_videos = youtube.playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                            maxResults=50, ).execute()  # Данные по видео из плейлиста

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                     self.playlist_videos['items']]  # все id видеороликов из плейлиста
        self.video_response = youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()  # Данные по видео

    @property
    def total_duration(self):
        """
        Получаем суммарную длительность видеороликов плейлиста h:min:sec (обращение как к свойству)
        """

        times = []

        for video in self.video_response['items']:  # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            times.append(str(duration))

        total_time = datetime.timedelta()

        for t in times:
            (h, m, s) = t.split(':')
            d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            total_time += d

        return total_time

    def total_seconds(self):
        """
        Получаем суммарную длительность видеороликов плейлиста в секундах
        """
        self.total_seconds = 0
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration_secs = isodate.parse_duration(iso_8601_duration).total_seconds()
            self.total_seconds += duration_secs
        return self.total_seconds

    def show_best_video(self):

        max_likes = 0
        best_video = None

        for video in self.video_response['items']:
            likes = int(video['statistics']['likeCount'])
            if likes > max_likes:
                best_video = video['id']

        return "https://youtu.be/" + best_video
