import tweepy

from flair.models import TextClassifier
classifier = TextClassifier.load("en-sentiment")
from flair.data import Sentence

class Message:
    def __init__(self, perception, popularity, platform):
        self.perception = perception
        self.popularity = popularity
        self.platform = platform

class Twitter:
    def __init__(self):
        consumer_key = "3Qss3R71D2jkhYFy5QfXeqBmE"
        consumer_secret = "B6NDgZktTtbd1PrwGCCizDIPXFSFdmvhAh4PfKT6cUFhKpj7Xg"
        access_token = "1459612052939427841-GTCsDujq0SqVuNvahK5HLhpQUMfHc9"
        access_token_secret = "1yLZuIt7nEByLDRXWlaI0GGBrWRCUOHoqVwctY3pYafec"
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def calculate_perception(self, topic):
        # # Twitter
        # twitterMessages = twitter.getMessages(topic)
        # twitter_sum = 0.0
        # twitter_perception = 0.0
        # for twitterMessage in twitterMessages:
        #     twitter_perception += ((twitterMessage.popularity + 1) * twitterMessage.perception)
        #     twitter_sum += (twitterMessage.popularity + 1)
        # if twitter_sum > 10000:
        #     twitter_val = 1
        # else:
        #     twitter_val = twitter_sum / 10000
        # twitter_perception = twitter_perception / twitter_sum
        pass

    def getMessages(self, topic):
        messages = list()
        for pages in tweepy.Cursor(
            self.api.search_tweets,
            q=topic,
            result_type="mixed",
            lang="en",
            tweet_mode="extended",
            since_id="1456942670778191874",
        ).items(50):
            sentence = Sentence(pages.full_text)
            classifier.predict(sentence)
            if sentence.labels[0].score < 0.8:
                perception = 0
            elif sentence.labels[0].value == "POSITIVE":
                perception = 1
            else:
                perception = -1
            message = Message(perception, pages.favorite_count, "Twitter")
            messages.append(message)
        return messages