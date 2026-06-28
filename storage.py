import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

_EMPTY = {"next_id": 1, "expenses": []}


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"next_id": 1, "expenses": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
