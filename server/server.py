# Make a flask server
from flask import Flask, request
import sqlite3
from scraper import Scraper

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route("/")
def home():
    return "Hello, World!"

# Post request to call scraper
@app.route("/api/v1/scraper", methods=["POST"])
def scraper():
    populated: bool = Scraper.populate_database()
    return {"success": populated}

# Get request with stock header
@app.route("/api/v1/stock", methods=["GET"])
def stock():
    ticker: str = request.args.get("ticker")
    conn: sqlite3.Connection = sqlite3.connect("local.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks WHERE ticker = ?", (ticker,))
    row = cursor.fetchone()

    if row:
        column_names = [column[0] for column in cursor.description]
        data = dict(zip(column_names, row))
        data['success'] = True
        return data
    else:
        return {"success": False}


if __name__ == "__main__":
    app.run()