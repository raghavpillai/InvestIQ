# Copyright 2022 Cartesi Pte. Ltd.
#
# SPDX-License-Identifier: Apache-2.0
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from os import environ
import logging
import requests
import dotenv
import sys
import sqlite3
sys.path.append("..")
from typing import List, Dict, Tuple

dotenv.load_dotenv()
logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

log_file = "file.log"
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
print("HI!!!!!!!!!")

rollup_server = environ["ROLLUP_HTTP_SERVER_URL"]
logger.info(f"HTTP rollup_server url is {rollup_server}")

notices = []

def handle_advance(data):
    logger.info(f"Received advance request data {data}")
    logger.info("Adding notice")
    notice = {"payload": data["payload"]}
    notices.append(notice)
    response = requests.post(rollup_server + "/notice", json=notice)
    logger.info(f"Received notice status {response.status_code} body {response.content}")
    return "accept"

def handle_inspect(data):
    logger.info(f"Received inspect request data {data}")
    logger.info("Adding report")
    report = {"payload": data["payload"]}
    notices.append(report)
    response = requests.post(rollup_server + "/report", json=report)
    logger.info(f"Received report status {response.status_code}")
    return "accept"

def return_leaderboard(data):
    conn: sqlite3.Connection = sqlite3.connect("local.db")
    cursor: sqlite3.Cursor = conn.cursor()
    
    # Top 5 perception
    cursor.execute("SELECT * FROM stocks ORDER BY perception DESC LIMIT 5")
    top_5_perception: List[Tuple[str, float]] = cursor.fetchall()

    # Bottom 5 perception
    cursor.execute("SELECT * FROM stocks ORDER BY perception ASC LIMIT 5")
    bottom_5_perception: List[Tuple[str, float]] = cursor.fetchall()

    # Top 5 overall rating
    cursor.execute("SELECT * FROM stocks ORDER BY overall_rating DESC LIMIT 5")
    top_5_overall_rating: List[Tuple[str, float]] = cursor.fetchall()

    column_names: List[str] = [column[0] for column in cursor.description]
    
    data: Dict[str, str] = {
        "success": True,
        "top_5_perception": [dict(zip(column_names, row)) for row in top_5_perception],
        "bottom_5_perception": [dict(zip(column_names, row)) for row in bottom_5_perception],
        "top_5_overall_rating": [dict(zip(column_names, row)) for row in top_5_overall_rating],
    }
    return data

handlers = {
    "advance_state": handle_advance,
    "inspect_state": handle_inspect,
}
print(return_leaderboard)

finish = {"status": "accept"}

while True:
    logger.info("Sending finish")
    response = requests.post(rollup_server + "/finish", json=finish)
    logger.info(f"Received finish status {response.status_code}")
    if response.status_code == 202:
        logger.info("No pending rollup request, trying again")
    else:
        rollup_request = response.json()
        data = rollup_request["data"]
        
        handler = handlers[rollup_request["request_type"]]
        finish["status"] = handler(rollup_request["data"])
