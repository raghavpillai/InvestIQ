from typing import List, Dict
from stock import Stock
import yfinance as yf
import pandas as pd
import sqlite3
import concurrent.futures

DATABASE_NAME = "local.db"
TABLE_NAME = "stocks"


class Scraper:

    @classmethod
    def populate_database(cls, overwrite: bool=False) -> bool:
        tickers: List[str] = cls._get_sp500_tickers()
        fields: Dict[str, str] = {
            "ticker": "TEXT PRIMARY KEY",
            "name": "TEXT",
            "market_cap": "FLOAT",
            "description": "TEXT",
            "similar": "TEXT",
            "current_price": "FLOAT",
            "growth": "TEXT",
            "recommend": "TEXT",
            "blurb": "TEXT",
            "logo_url": "TEXT",
            "analyst_count": "INT",
            "perception": "FLOAT",
            "popularity": "INT",
            "overall_rating": "FLOAT",
            "titles": "TEXT"
        }

        # Connect to the SQLite database
        conn: sqlite3.Connection = sqlite3.connect(DATABASE_NAME)

        # Create a table if it doesn't exist
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} ({','.join([f'{name} {value}' for name, value in fields.items()])})"
        conn.execute(create_table_sql)
        conn.commit()
        conn.close()

        def process_ticker(ticker: str) -> None:
            conn: sqlite3.Connection = sqlite3.connect(DATABASE_NAME) # Threads!
            if not overwrite and conn.execute(f"SELECT * FROM {TABLE_NAME} WHERE ticker = ?", (ticker,)).fetchone():
                return
            try:
                cls.send_to_database(ticker, conn)
            except Exception as e:
                print(e)
                print(f"Unable to write stock info for {ticker}")

        # with concurrent.futures.ThreadPoolExecutor() as executor:
        #     executor.map(process_ticker, tickers)
        for ticker in tickers:
            process_ticker(ticker)
            
        return True

    @classmethod
    def send_to_database(cls, stock_ticker: str, conn: sqlite3.Connection) -> None:
        stock: Stock = Stock(stock_ticker)
        stock.populate()
        conn.execute(
            f"INSERT OR REPLACE INTO {TABLE_NAME} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (
                stock_ticker,
                stock.name,
                stock.market_cap,
                stock.description,
                str(stock.similar),
                stock.current_price,
                stock.growth,
                stock.recommend,
                stock.blurb,
                stock.logo,
                stock.analyst_count,
                stock.perception,
                stock.popularity,
                stock.overall_rating,
                str(stock.titles)
            )
        )
        conn.commit()
        conn.close()

    @classmethod
    def _get_sp500_tickers(cls) -> List[str]:
        table: pd.DataFrame = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        
        tickers: List[str] = table['Symbol'].tolist()
        import random
        random.shuffle(tickers)

        return tickers[:10]

if __name__ == "__main__":
    tickers = Scraper.populate_database(overwrite=False)
    print(tickers)
