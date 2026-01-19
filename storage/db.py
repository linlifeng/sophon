import json
from pathlib import Path

DB_FILE = Path("memory.json")

def save(data):
    DB_FILE.write_text(json.dumps(data, indent=2))

def load():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text())
    return {}
