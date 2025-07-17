# app/utils.py

import json
from datetime import datetime
from pathlib import Path

def save_json(data, filename="output/business_ideas.json"):
    Path("output").mkdir(exist_ok=True)
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def timestamp():
    return datetime.now().isoformat()
