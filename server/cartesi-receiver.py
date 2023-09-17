# Make a flask server
import sqlite3
from typing import Tuple, Dict, List
from flask import Flask, request
from scraper import Scraper
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Post request to call scraper
@app.route("/api/v1/scraper", methods=["POST"])
def scraper() -> Dict[str, bool]:
    print("Called")

if __name__ == "__main__":
    app.run()