import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')  # API_KEY скопирован из гугла и вставлен в переменные окружения
    youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel_info = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = ''
        self.description = ''
        self.url = ''
        self.subscriber_count = 0
        self.video_count = 0
        self.view_count = 0

        api_key: str = os.getenv('YT_API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        if channel['items']:
            channel = channel['items'][0]
            self.title = channel['snippet']['title']
            self.description = channel['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.channel_id}"
            self.subscriber_count = channel['statistics']['subscriberCount']
            self.video_count = channel['statistics']['videoCount']
            self.view_count = channel['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other) -> int:
        """Метод сложения"""
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other) -> int:
        """Метод вычитания"""
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __gt__(self, other) -> int:
        """Метод сложения"""
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other) -> int:
        """Метод сложения"""
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __lt__(self, other) -> int:
        """Метод сложения"""
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other) -> int:
        """Метод сложения"""
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __eq__(self, other) -> int:
        """Метод сложения"""
        return int(self.subscriber_count) == int(other.subscriber_count)

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        self.__channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel_info, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        """возвращающий объект для работы с YouTube API"""
        api_key: str = os.getenv('YT_API_KEY')  # API_KEY скопирован из гугла и вставлен в переменные окружения
        youtube = build('youtube', 'v3', developerKey=api_key)  # создать специальный объект для работы с API
        return youtube

    def to_json(self, file_name):
        """сохраняющий в файл значения атрибутов экземпляра `Channel`"""
        data = {
            'channel_id': self.channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
