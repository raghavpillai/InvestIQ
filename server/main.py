import tweepy
import praw
import os
import yfinance as yf
import requests
import dotenv

from newsapi import NewsApiClient

from apiclient.discovery import build

from flair.models import TextClassifier
from flair.data import Sentence

dotenv.load_dotenv()
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_APP_ID = os.getenv("REDDIT_APP_ID")
REDDIT_APP_SECRET = os.getenv("REDDIT_APP_SECRET")


YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


class Message:
    def __init__(self, perception, popularity, platform):
        self.perception = perception
        self.popularity = popularity
        self.platform = platform


class Stock:
    def __init__(self, perception, popularity, rating):
        self.perception = perception
        self.popularity = popularity
        self.rating = rating


classifier = TextClassifier.load("en-sentiment")

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


class Twitter:
    def __init__(self):
        consumer_key = "3Qss3R71D2jkhYFy5QfXeqBmE"
        consumer_secret = "B6NDgZktTtbd1PrwGCCizDIPXFSFdmvhAh4PfKT6cUFhKpj7Xg"
        access_token = "1459612052939427841-GTCsDujq0SqVuNvahK5HLhpQUMfHc9"
        access_token_secret = "1yLZuIt7nEByLDRXWlaI0GGBrWRCUOHoqVwctY3pYafec"
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

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


class Youtube:
    def __init__(self):
        self.youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

    def getMessages(self, topic):
        messages = list()
        title_request = self.youtube.search().list(
            q=topic,
            part="snippet",
            type="video",
            publishedAfter="2021-11-07T00:00:00Z",
            maxResults=100,
        )
        res1 = title_request.execute()
        ids = ""
        titles = list()
        for item in res1["items"]:
            titles.append(item["snippet"]["title"])
            ids = ids + str(item["id"]["videoId"]) + ","
        ids = ids[:-1]
        statistics_request = self.youtube.videos().list(
            id=ids, part="statistics", maxResults=100
        )
        res2 = statistics_request.execute()
        index = 0
        for item in res2["items"]:
            title = titles[index]
            sentence = Sentence(title)
            classifier.predict(sentence)
            if sentence.labels[0].score < 0.8:
                perception = 0
            elif sentence.labels[0].value == "POSITIVE":
                perception = 1
            else:
                perception = -1
            print(item["statistics"])

            views = int(item["statistics"]["viewCount"])
            if "likeCount" in item["statistics"]:
                likes = int(item["statistics"]["likeCount"])
                dislikes = (
                    likes * 0.3
                )  # Temp solution, b4 int(item['statistics']['dislikeCount'])
                if dislikes == 0:
                    likeDislikeRatio = 1
                else:
                    likeDislikeRatio = likes / (dislikes + likes)
            else:
                likeDislikeRatio = 1
            perception *= likeDislikeRatio
            message = Message(perception, views, "Youtube")
            messages.append(message)
            index += 1
        return messages


class News:
    def __init__(self):
        key = "67e2b64352e14eb4af0a5517e50e6379"
        self.api = NewsApiClient(api_key=key)

    def getMessages(self, topic):
        messages = list()
        all_articles = self.api.get_everything(
            qintitle=topic,
            from_param="2023-09-03",
            to="2023-09-03",
            language="en",
            page_size=100,
        )
        for article in all_articles.get("articles"):
            sentence = Sentence(article.get("title"))
            classifier.predict(sentence)
            if sentence.labels[0].score < 0.8:
                perception = 0
            elif sentence.labels[0].value == "POSITIVE":
                perception = 1
            else:
                perception = -1
            message = Message(perception, all_articles.get("totalResults"), "News")
            messages.append(message)
        return messages


def testing():
    stock_tkr = "AAPL"
    # Find the stock information
    

    response = requests.get(
        "https://api.polygon.io/v1/meta/symbols/"
        + stock_tkr
        + "/company?apiKey=0ip9Jo9miAua0zJYVDvjjDIAluVzRJJX"
    )

    stock_details = response.json()

    stock_raw = yf.Ticker(stock_tkr)
    stock_data = stock_raw.info

    print(stock_details)

    name = stock_details["name"]
    market_cap = stock_details["marketcap"]
    similar = stock_details["similar"]
    print(stock_data)

    description = stock_data["longBusinessSummary"]
    current_price = stock_data["currentPrice"]
    open_price = stock_data["regularMarketOpen"]
    close_price = stock_data["previousClose"]
    # logo = stock_data["logo_url"]
    growth = stock_data["earningsGrowth"]
    recommend = stock_data["recommendationMean"]

    topic = name

    # twitter = Twitter()
    reddit = Reddit()
    news = News()
    youtube = Youtube()

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

    # Reddit
    redditMessages = reddit.getMessages(topic)
    reddit_sum = 0.0
    reddit_perception = 0.0
    for redditMessage in redditMessages:
        reddit_perception += (redditMessage.popularity + 1) * redditMessage.perception
        reddit_sum += redditMessage.popularity + 1
    if reddit_sum > 10000:
        reddit_val = 1
    else:
        reddit_val = reddit_sum / 10000
    reddit_perception = reddit_perception / reddit_sum

    # Youtube
    youtubeMessages = youtube.getMessages(topic)
    youtube_sum = 0.0
    youtube_perception = 0.0
    for youtubeMessage in youtubeMessages:
        youtube_perception += (
            youtubeMessage.popularity + 1
        ) * youtubeMessage.perception
        youtube_sum += youtubeMessage.popularity + 1
    if youtube_sum > 10000000:
        youtube_val = 1
    else:
        youtube_val = youtube_sum / 10000000
    youtube_perception = youtube_perception / youtube_sum

    # News
    newsMessages = news.getMessages(topic)

    if len(newsMessages) == 0:
        news_val = 0
    elif newsMessages[0].popularity > 5000:
        news_val = 1
    else:
        news_val = newsMessages[0].popularity / 5000
    news_perception = 0.0
    for newsMessage in newsMessages:
        news_perception += newsMessage.perception
    if len(newsMessages) == 0:
        news_perception = 0
    else:
        news_perception = news_perception / len(newsMessages)
    total_score = ((((reddit_val + youtube_val) / 2) + news_val) / 1.25) + 0.3
    total_perception = (
        (((reddit_perception + youtube_val) / 2) + news_perception) / 2
    ) + 0.2

    import math

    overall_rating = (
        abs(total_perception)
        / total_perception
        * pow(math.tanh(8 * total_score * total_perception), 2)
    )  # Overall Rating = tanh^2(constant * popularity * perception) * 100 * -1 if perception is negative, this gives a range from [-100, 100]
    stock = Stock(
        round(total_perception, 2),
        round(total_score * 100, 2),
        round(overall_rating * 100, 2),
    )

    print("Getting values for stock: " + name)


testing()
