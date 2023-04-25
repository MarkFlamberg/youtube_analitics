import json
from googleapiclient.discovery import build

API_KEY = 'AIzaSyDJWt5EPHCXi5Y5uS5WyzTzfDuoqTN2iZQ'


def get_youtube():
    youtube = build('youtube', 'v3', developerKey=API_KEY)  # создать специальный объект для работы с API
    return youtube


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.channel_id

        channel = get_youtube().channels().list(id=channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))
