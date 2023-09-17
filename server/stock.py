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

        # Data
        self.perception: float = None
        self.popularity: int = None
        self.overall_rating: float = None

    def create_blurb(self, stock_data: Dict[str, str]) -> str:
        # Delete to save tokens
        del stock_data["longBusinessSummary"]
        del stock_data["companyOfficers"]
        del stock_data["uuid"]
        del stock_data["messageBoardId"]

        response: Dict[str, str] = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant designed to take in stock data and return an smart but concise analysis on the market trends. Use and cite quantitative data to determine if the stock is worth buying or not. Every sentence should be a point backed up by data. Provide a single concise paragraph blurb of no more than 150 characters.",
                },
                {
                    "role": "user",
                    "content": "{'address1': '3M Center', 'city': 'Saint Paul', 'state': 'MN', 'zip': '55144-1000', 'country': 'United States', 'phone': '651 733 1110', 'website': 'https://www.3m.com', 'industry': 'Conglomerates', 'industryDisp': 'Conglomerates', 'sector': 'Industrials', 'sectorDisp': 'Industrials', 'longBusinessSummary': '3M Company provides diversified technology services in the United States and internationally. The company operates through four segments: Safety and Industrial; Transportation and Electronics; Health Care; and Consumer. The Safety and Industrial segment offers industrial abrasives and finishing for metalworking applications; autobody repair solutions; closure systems for personal hygiene products, masking, and packaging materials; electrical products and materials for construction and maintenance, power distribution, and electrical original equipment manufacturers; structural adhesives and tapes; respiratory, hearing, eye, and fall protection solutions; and natural and color-coated mineral granules for shingles. The Transportation and Electronics segment provides ceramic solutions; attachment tapes, films, sound, and temperature management for transportation vehicles; premium large format graphic films for advertising and fleet signage; light management films and electronics assembly solutions; packaging and interconnection solutions; and reflective signage for highway, and vehicle safety. The Healthcare segment offers health care procedure coding and reimbursement software; skin, wound care, and infection prevention products and solutions; dentistry and orthodontia solutions; and filtration and purification systems. The Consumer segment provides consumer bandages, braces, supports, and consumer respirators; cleaning products for the home; retail abrasives, paint accessories, car care DIY products, picture hanging, and consumer air quality solutions; and stationery products. It offers its products through e-commerce and traditional wholesalers, retailers, jobbers, distributors, and dealers. 3M Company was founded in 1902 and is headquartered in St. Paul, Minnesota.', 'fullTimeEmployees': 92000, 'companyOfficers': [{'maxAge': 1, 'name': 'Mr. Michael F. Roman', 'age': 62, 'title': 'Chairman & CEO', 'yearBorn': 1960, 'fiscalYear': 2022, 'totalPay': 3030438, 'exercisedValue': 474479, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Monish D. Patolawala', 'age': 50, 'title': 'Exec. VP & CFO', 'yearBorn': 1972, 'fiscalYear': 2022, 'totalPay': 2086773, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Jeffrey R. Lavers', 'age': 58, 'title': 'Group Pres of Health Care', 'yearBorn': 1964, 'fiscalYear': 2022, 'totalPay': 1097614, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Peter D. Gibbons', 'age': 61, 'title': 'Group Pres of Enterprise Operations', 'yearBorn': 1961, 'fiscalYear': 2022, 'totalPay': 1333946, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Ms. Theresa E. Reinseth', 'age': 49, 'title': 'Sr. VP, Corp. Controller & Chief Accounting Officer', 'yearBorn': 1973, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Dr. John P. Banovetz', 'age': 54, 'title': 'Exec. VP, CTO & Environmental Responsibility', 'yearBorn': 1968, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Mark W. Murphy II', 'age': 54, 'title': 'Exec. VP and Chief Information & Digital Officer', 'yearBorn': 1968, 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Bruce  Jermeland C.F.A.', 'title': 'VP of Investor Relations', 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Michael A. Duran', 'title': 'Sr. VP and Chief Ethics & Compliance Officer', 'exercisedValue': 0, 'unexercisedValue': 0}, {'maxAge': 1, 'name': 'Mr. Kevin H. Rhodes', 'age': 59, 'title': 'Exec. VP & Chief Legal Affairs Officer', 'yearBorn': 1963, 'exercisedValue': 0, 'unexercisedValue': 0}], 'auditRisk': 8, 'boardRisk': 7, 'compensationRisk': 7, 'shareHolderRightsRisk': 4, 'overallRisk': 7, 'governanceEpochDate': 1693526400, 'compensationAsOfEpochDate': 1672444800, 'maxAge': 86400, 'priceHint': 2, 'previousClose': 102.32, 'open': 101.89, 'dayLow': 100.65, 'dayHigh': 102.41, 'regularMarketPreviousClose': 102.32, 'regularMarketOpen': 101.89, 'regularMarketDayLow': 100.65, 'regularMarketDayHigh': 102.41, 'dividendRate': 6.0, 'dividendYield': 0.0586, 'exDividendDate': 1692316800, 'fiveYearAvgDividendYield': 3.83, 'beta': 0.968188, 'forwardPE': 10.407826, 'volume': 6002111, 'regularMarketVolume': 6002111, 'averageVolume': 3708340, 'averageVolume10days': 4066940, 'averageDailyVolume10Day': 4066940, 'bid': 101.06, 'ask': 101.29, 'bidSize': 800, 'askSize': 900, 'marketCap': 55784308736, 'fiftyTwoWeekLow': 92.38, 'fiftyTwoWeekHigh': 133.91, 'priceToSalesTrailing12Months': 1.687672, 'fiftyDayAverage': 104.1908, 'twoHundredDayAverage': 108.2074, 'trailingAnnualDividendRate': 5.98, 'trailingAnnualDividendYield': 0.058444098, 'currency': 'USD', 'enterpriseValue': 69124866048, 'profitMargins': -0.044320002, 'floatShares': 551495637, 'sharesOutstanding': 551992000, 'sharesShort': 11899822, 'sharesShortPriorMonth': 10500010, 'sharesShortPreviousMonthDate': 1690761600, 'dateShortInterest': 1693440000, 'sharesPercentSharesOut': 0.0216, 'heldPercentInsiders': 0.00125, 'heldPercentInstitutions': 0.67402, 'shortRatio': 3.54, 'shortPercentOfFloat': 0.0216, 'impliedSharesOutstanding': 551992000, 'bookValue': 14.127, 'priceToBook': 7.1536775, 'lastFiscalYearEnd': 1672444800, 'nextFiscalYearEnd': 1703980800, 'mostRecentQuarter': 1688083200, 'netIncomeToCommon': -1464999936, 'trailingEps': -2.85, 'forwardEps': 9.71, 'lastSplitFactor': '2:1', 'lastSplitDate': 1064880000, 'enterpriseToRevenue': 2.091, 'enterpriseToEbitda': 9.255, '52WeekChange': -0.13357341, 'SandP52WeekChange': 0.14113986, 'lastDividendValue': 1.5, 'lastDividendDate': 1692316800, 'exchange': 'NYQ', 'quoteType': 'EQUITY', 'symbol': 'MMM', 'underlyingSymbol': 'MMM', 'shortName': '3M Company', 'longName': '3M Company', 'firstTradeDateEpochUtc': -252322200, 'timeZoneFullName': 'America/New_York', 'timeZoneShortName': 'EDT', 'uuid': '375388b3-dab7-3763-90cd-457ad19388a2', 'messageBoardId': 'finmb_289194', 'gmtOffSetMilliseconds': -14400000, 'currentPrice': 101.06, 'recommendationKey': 'none', 'totalCash': 4313999872, 'totalCashPerShare': 7.815, 'ebitda': 7469000192, 'totalDebt': 16899999744, 'quickRatio': 0.847, 'currentRatio': 1.441, 'totalRevenue': 33053999104, 'debtToEquity': 215.095, 'revenuePerShare': 59.359, 'returnOnAssets': 0.074650005, 'returnOnEquity': -0.13371, 'grossProfits': 15000000000, 'freeCashflow': 3877499904, 'operatingCashflow': 6237000192, 'revenueGrowth': -0.043, 'grossMargins': 0.44134, 'ebitdaMargins': 0.22596, 'operatingMargins': 0.17075, 'financialCurrency': 'USD', 'trailingPegRatio': 3.8743}",
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

        self.description = stock_data.get("longBusinessSummary")
        self.current_price = stock_data.get("currentPrice")
        open_price = stock_data.get("regularMarketOpen")
        close_price = stock_data.get("previousClose")
        # logo = stock_data.get("logo_url")
        self.growth = stock_data.get("earningsGrowth")
        self.recommend = stock_data.get("recommendationMean")

        self.blurb = self.create_blurb(stock_data)

        # twitter = Twitter()
        reddit = Reddit()
        news = News()
        youtube = Youtube()

        reddit_perception, reddit_popularity = reddit.calculate_perception(self.ticker)
        youtube_perception, youtube_popularity = youtube.calculate_perception(
            self.ticker
        )
        news_perception, news_popularity = news.calculate_perception(self.ticker)

        total_score = (
            (((reddit_popularity + youtube_popularity) / 2) + news_popularity) / 1.25
        ) + 0.3
        total_perception = (
            (((reddit_perception + youtube_popularity) / 2) + news_perception) / 2
        ) + 0.2

        overall_rating = (
            abs(total_perception)
            / total_perception
            * pow(math.tanh(8 * total_score * total_perception), 2)
        )  # Overall Rating = tanh^2(constant * popularity * perception) * 100 * -1 if perception is negative, this gives a range from [-100, 100]

        self.perception: float = round(total_perception, 2)
        self.popularity: float = round(total_score * 100, 2)
        self.overall_rating: float = round(overall_rating * 100, 2)

    def get_rating(self) -> float:
        if self.overall_rating is None:
            print("Unable to get rating")
            return 0
        return self.overall_rating

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
    print(stock.perception)
    print(stock.total_score)
    print(stock.rating)
