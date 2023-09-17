import yfinance as yf
import requests
import dotenv
import os
import math
import openai
from typing import List, Dict

dotenv.load_dotenv()
from sources.news import News
from sources.reddit import Reddit
from sources.youtube import Youtube

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")


class Stock:
    def __init__(self, ticker):
        # Essentials
        self.ticker: str = ticker

        # Details
        self.name: str = None
        self.market_cap: float = None
        self.description: str = None
        self.similar: str = None
        self.current_price: float = None
        self.growth: str = None
        self.recommend: str = None
        self.blurb: str = None
        self.logo_url: str = None
        self.analyst_count: int = None

        # Data
        self.perception: float = None
        self.popularity: int = None
        self.overall_rating: float = None

    def create_blurb(self, stock_data: Dict[str, str]) -> str:
        # Delete to save tokens
        stuff_to_delete: List[str] = [
            "longBusinessSummary", "companyOfficers", "uuid", "messageBoardId",
            "address1", "website", "phone", "city", "state", "zip",
            "country", "industry", "gmtOffSetMilliseconds", "governanceEpochDate",
            "timeZoneFullName", "timeZoneShortName",
        ]

        for stuff in stuff_to_delete:
            if stuff in stock_data:
                del stock_data[stuff]
        
        stock_data["name"] = self.name
        
        return "Insert blurb here"

        response: Dict[str, str] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to take in stock data and return an smart but concise analysis on the market trends. Use and cite quantitative data to determine if the stock is worth buying or not. Every sentence should be a point backed up by data. Provide a single concise paragraph blurb of no more than 150 characters.",
                },
                {
                    "role": "user",
                    "content": str(stock_data),
                }
            ],
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    def populate(self):
        if not self.ticker:
            print("Invalid ticker")
            return

        stock_details: Dict[str, str] = {}
        stock_data: Dict[str, str] = {}
        try:
            stock_details, stock_data = self._get_stock_info()
        except Exception:
            print("Unable to get stock info")
            return

        print(f"Retrieving stock info for {self.ticker}")

        self.name = stock_details.get("name")
        self.market_cap = stock_details.get("marketcap")
        self.similar = stock_details.get("similar")
        self.logo = stock_details.get("logo")
        print(stock_details)

        open_price = stock_data.get("regularMarketOpen")
        close_price = stock_data.get("previousClose")
        self.description = stock_data.get("longBusinessSummary")
        self.current_price = stock_data.get("currentPrice")
        self.growth = stock_data.get("revenueGrowth",0) * 100
        self.recommend = stock_data.get("recommendationKey", "Unknown")
        self.analyst_count = stock_data.get("numberOfAnalystOpinions", 0)

        self.blurb = self.create_blurb(stock_data)

        # twitter = Twitter()
        reddit: Reddit = Reddit()
        news: News = News()
        youtube: Youtube = Youtube()

        reddit_perception, reddit_popularity = reddit.calculate_perception(self.name)
        youtube_perception, youtube_popularity = youtube.calculate_perception(
            self.name
        )
        news_perception, news_popularity = news.calculate_perception(self.name)

        total_score: float = (
            (((reddit_popularity + youtube_popularity) / 2) + news_popularity) / 1.25
        ) + 0.3
        total_perception: float = (
            (((reddit_perception + youtube_popularity) / 2) + news_perception) / 2
        ) + 0.2

        overall_rating: float = (
            abs(total_perception)
            / total_perception
            * pow(math.tanh(8 * total_score * total_perception), 2)
        )  # Overall Rating = tanh^2(constant * popularity * perception) * 100 * -1 if perception is negative, this gives a range from [-100, 100]

        self.perception: float = round(total_perception, 2)
        self.popularity: float = round(total_score * 100, 2)
        self.overall_rating: float = round(overall_rating * 100, 2)

    def _get_stock_info(self) -> Dict[str, str]:
        response: requests.Response = requests.get(
            f"https://api.polygon.io/v1/meta/symbols/{self.ticker}/company?apiKey={POLYGON_API_KEY}",
        )
        stock_details: Dict[str, str] = response.json()

        stock_raw: yf.Ticker = yf.Ticker(self.ticker)
        stock_data: Dict[str, str] = stock_raw.info
        return stock_details, stock_data


if __name__ == "__main__":
    stock = Stock("AAPL")
    stock.populate()