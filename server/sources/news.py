import os
from typing import List
from newsapi import NewsApiClient
from flair.models import TextClassifier
from flair.data import Sentence

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

classifier: TextClassifier = TextClassifier.load("en-sentiment")


class Message:
    def __init__(self, perception: float, popularity: int, platform: str) -> None:
        self.perception: float = perception
        self.popularity: int = popularity
        self.platform: str = platform


class News:
    def __init__(self) -> None:
        self.api: NewsApiClient = NewsApiClient(api_key=NEWS_API_KEY)

    def calculate_perception(self, stock_ticker: str) -> float:
        news_messages: List[Message] = self.get_messages(stock_ticker)

        if not news_messages:
            value: float = 0
        elif news_messages[0].popularity > 5000:
            value: float = 1
        else:
            value: float = news_messages[0].popularity / 5000
        
        perception: float = 0.0
        for message in news_messages:
            perception += message.perception
        
        if not news_messages:
            perception = 0
        else:
            perception = perception / len(news_messages)
        
        return perception, value

    def get_messages(self, topic: str) -> List[Message]:
        messages: List[Message] = []
        all_articles: dict = self.api.get_everything(
            qintitle=topic,
            from_param="2023-09-03",
            to="2023-09-03",
            language="en",
            page_size=100,
        )
        for article in all_articles.get("articles", []):
            perception: float = self._calculate_perception(article.get("title", ""))
            total_results: int = all_articles.get("totalResults", 0)
            message: Message = Message(perception, total_results, "News")
            messages.append(message)
        return messages

    @staticmethod
    def _calculate_perception(title: str) -> float:
        sentence: Sentence = Sentence(title)
        classifier.predict(sentence)
        label = sentence.labels[0]

        if label.score < 0.8:
            return 0
        elif label.value == "POSITIVE":
            return 1
        else:
            return -1
