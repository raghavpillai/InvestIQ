from typing import List, Dict
from stock import Stock
import yfinance as yf
import pandas as pd
import sqlite3
import concurrent.futures

class Scraper:

    @classmethod
    def populate_database(cls, overwrite: bool=False) -> bool:
        tickers: List[str] = cls._get_sp500_tickers()
        conn: sqlite3.Connection = sqlite3.connect("local.db")
        conn.execute("CREATE TABLE IF NOT EXISTS stocks (ticker TEXT, score FLOAT)")
        conn.commit()
        conn.close()

        def process_ticker(ticker: str) -> None:
            conn: sqlite3.Connection = sqlite3.connect("local.db")
            if not overwrite and not conn.execute("SELECT * FROM stocks WHERE ticker = ?", (ticker,)).fetchone():
                return
            try:
                cls.send_to_database(ticker, conn)
            except Exception as e:
                print(e)
                print(f"Unable to write stock info for {ticker}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_ticker, tickers)
            
        return True

    @classmethod
    def send_to_database(cls, stock_ticker: str, conn: sqlite3.Connection) -> None:
        stock = Stock(stock_ticker)
        stock.populate()
        score: float = stock.get_rating()
        print(score)
        conn.execute(
            "INSERT INTO stocks (ticker, score) VALUES (?, ?)", (stock_ticker, score)
        )
        conn.commit()

    @classmethod
    def _get_sp500_tickers(cls) -> List[str]:
        table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
        
        tickers = table['Symbol'].tolist()
        return tickers[:1]

if __name__ == "__main__":
    tickers = Scraper.populate_database(overwrite=True)
    print(tickers)
