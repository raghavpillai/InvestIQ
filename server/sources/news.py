import os
from typing import List
from newsapi import NewsApiClient
from sources.lib.message import Message
import sources.lib.perception as perc

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

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

    def get_messages(self, company_name: str) -> List[Message]:
        messages: List[Message] = []
        all_articles: dict = self.api.get_everything(
            qintitle=f"{company_name} stock",
            from_param="2023-08-17",
            to="2023-09-17",
            language="en",
            page_size=100,
        )
        
        for article in all_articles.get("articles", []):
            perception: float = perc.calculate_perception(article.get("title", ""))
            total_results: int = all_articles.get("totalResults", 0)
            message: Message = Message(perception, total_results, "News", article.get("title", ""))
            messages.append(message)
        
        messages.sort(key=lambda x: x.perception)
        self.top_titles: List[str] = [message.content for message in messages[-3:]]
        self.bottom_titles: List[str] = [message.content for message in messages[:3]]

        return messages
    