import praw
import os

REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_APP_ID = os.getenv("REDDIT_APP_ID")
REDDIT_APP_SECRET = os.getenv("REDDIT_APP_SECRET")

from flair.models import TextClassifier
classifier = TextClassifier.load("en-sentiment")
from flair.data import Sentence

class Message:
    def __init__(self, perception, popularity, platform):
        self.perception = perception
        self.popularity = popularity
        self.platform = platform

class Reddit:
    def __init__(self):
        username = REDDIT_USERNAME
        password = REDDIT_PASSWORD
        app_id = REDDIT_APP_ID
        app_secret = REDDIT_APP_SECRET
        self.reddit = praw.Reddit(
            user_agent="Comment Extraction",
            client_id=app_id,
            client_secret=app_secret,
            username=username,
            password=password,
        )
        self.subreddit = self.reddit.subreddit("all")

    def getMessages(self, topic):
        messages = list()
        for submission in self.subreddit.search(
            query=topic, sort="relevance", time_filter="week"
        ):
            sentence = Sentence(submission.title)
            classifier.predict(sentence)
            if sentence.labels[0].score < 0.8:
                perception = 0
            elif sentence.labels[0].value == "POSITIVE":
                perception = 1
            else:
                perception = -1
            message = Message(perception, submission.score, "Reddit")
            messages.append(message)
        return messages