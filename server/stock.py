import yfinance as yf
import requests
import dotenv
import os
import math

dotenv.load_dotenv()
from sources.news import News
from sources.reddit import Reddit
from sources.youtube import Youtube

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")

class Stock:
    def __init__(self, name):
        self.name = name

    def populate(self):
        stock_tkr = self.name
        
        response = requests.get(
            "https://api.polygon.io/v1/meta/symbols/"
            + stock_tkr
            + f"/company?apiKey={POLYGON_API_KEY}",
        )

        stock_details = response.json()

        stock_raw = yf.Ticker(stock_tkr)
        stock_data = stock_raw.info

        name = stock_details["name"]
        market_cap = stock_details["marketcap"]
        similar = stock_details["similar"]

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
        redditMessages = reddit.get_messages(name)
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
        youtubeMessages = youtube.get_messages(name)
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
        newsMessages = news.get_messages(name)

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
        
        overall_rating = (
            abs(total_perception)
            / total_perception
            * pow(math.tanh(8 * total_score * total_perception), 2)
        )  # Overall Rating = tanh^2(constant * popularity * perception) * 100 * -1 if perception is negative, this gives a range from [-100, 100]
        
        self.perception = round(total_perception, 2)
        self.total_score = round(total_score * 100, 2)
        self.rating = overall_rating * 100, 2
        
        print("Getting values for stock: " + name)


if __name__ == "__main__":
    stock = Stock("AAPL")
    stock.populate()
    print(stock.perception)
    print(stock.total_score)
    print(stock.rating)