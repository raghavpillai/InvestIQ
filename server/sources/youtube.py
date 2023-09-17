import os
from typing import List, Dict
from apiclient.discovery import build
from sources.lib.message import Message
import sources.lib.perception as perc

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class Youtube:
    def __init__(self):
        self.youtube: build = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    def calculate_perception(self, stock_ticker: str) -> float:
        messages: List[Message] = self.get_messages(stock_ticker)
        total_sum: float = 0
        perception: float = 0
        for message in messages:
            perception += (message.popularity + 1) * message.perception
            total_sum += (message.popularity + 1)
        
        if total_sum > 10000000:
            value: float = 1
        else:
            value: float = total_sum / 10000000
        perception = perception / total_sum
        
        return perception, value
    
    def get_messages(self, company_name: str) -> List[Message]:
        messages: List[Message] = []
        titles: List[str] = []
        video_ids: List[str] = []
        titles, video_ids = self._fetch_video_titles_and_ids(f"{company_name} stock")
        video_statistics: List[dict] = self._fetch_video_statistics(video_ids)

        for index, stats in enumerate(video_statistics):
            title: str = titles[index]
            perception: float = perc.calculate_perception(title)
            popularity: int = int(stats["statistics"]["viewCount"])

            if "likeCount" in stats["statistics"]:
                likes: int = int(stats["statistics"]["likeCount"])
                dislikes: int = likes * 0.3  # Temp solution
                like_dislike_ratio: float = self._calculate_like_dislike_ratio(
                    likes, dislikes
                )
            else:
                like_dislike_ratio: float = 1

            perception *= like_dislike_ratio
            message: Message = Message(perception, popularity, "YouTube", title)
            messages.append(message)
        
        self.top_titles: List[str] = [message.content for message in messages[-3:]]
        self.bottom_titles: List[str] = [message.content for message in messages[:3]]

        return messages

    def _fetch_video_titles_and_ids(self, company_name: str) -> (List[str], List[str]):
        title_request: build = self.youtube.search().list(
            q=company_name,
            part="snippet",
            type="video",
            publishedAfter="2021-11-07T00:00:00Z",
            maxResults=100,
        )
        response: Dict[str, List[dict]] = title_request.execute()
        titles: List[str] = [item["snippet"]["title"] for item in response["items"]]
        video_ids: List[str] = [item["id"]["videoId"] for item in response["items"]]
        return titles, video_ids

    def _fetch_video_statistics(self, video_ids: List[str]) -> List[dict]:
        ids_str: str = ",".join(video_ids)
        statistics_request = self.youtube.videos().list(
            id=ids_str, part="statistics", maxResults=100
        )
        response: Dict[str, List[Dict]] = statistics_request.execute()
        return response["items"]

    @staticmethod
    def _calculate_like_dislike_ratio(likes: int, dislikes: int) -> float:
        if dislikes == 0:
            return 1
        return likes / (dislikes + likes)
