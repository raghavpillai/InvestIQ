import os
import praw
from typing import List
from flair.models import TextClassifier
from flair.data import Sentence

REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_APP_ID = os.getenv("REDDIT_APP_ID")
REDDIT_APP_SECRET = os.getenv("REDDIT_APP_SECRET")

classifier: TextClassifier = TextClassifier.load("en-sentiment")


class Message:
    def __init__(self, perception: float, popularity: int, platform: str):
        self.perception: float = perception
        self.popularity: int = popularity
        self.platform: str = platform


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
        else:
            value: float = total_sum / 10000
        perception = perception / total_sum
        
        return perception, value

    def get_messages(self, stock_ticker: str) -> List[Message]:
        messages: List[Message] = []
        for submission in self.subreddit.search(
            query=stock_ticker, sort="relevance", time_filter="week"
        ):
            perception: float = self._calculate_perception(submission.title)
            message: Message = Message(perception, submission.score, "Reddit")
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
