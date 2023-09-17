import os
import praw
from typing import List
from sources.lib.message import Message
import sources.lib.perception as perc

REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_APP_ID = os.getenv("REDDIT_APP_ID")
REDDIT_APP_SECRET = os.getenv("REDDIT_APP_SECRET")


class Reddit:
    def __init__(self):
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction",
            client_id=REDDIT_APP_ID,
            client_secret=REDDIT_APP_SECRET,
            username=REDDIT_USERNAME,
            password=REDDIT_PASSWORD,
        )
        self.subreddit: praw.models.Subreddit = self.reddit.subreddit("all")

    def calculate_perception(self, stock_ticker: str) -> float:
        messages: List[Message] = self.get_messages(stock_ticker)
        total_sum: float = 0
        perception: float = 0
        for message in messages:
            perception += (message.popularity + 1) * message.perception
            total_sum += (message.popularity + 1)
        
        if total_sum > 10000:
            value: float = 1
        elif total_sum == 0:
            return 0,0
        else:
            value: float = total_sum / 10000
        
        perception = perception / total_sum
        return perception, value

    def get_messages(self, company_name: str) -> List[Message]:
        messages: List[Message] = []
        for submission in self.subreddit.search(
            query=f"{company_name} stock", sort="relevance", time_filter="week"
        ):
            perception: float = perc.calculate_perception(submission.title)
            message: Message = Message(perception, submission.score, "Reddit", submission.title)
            messages.append(message)

        messages.sort(key=lambda x: x.perception)
        self.top_titles: List[str] = [message.content for message in messages[-3:]]
        self.bottom_titles: List[str] = [message.content for message in messages[:3]]

        return messages
