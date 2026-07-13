import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

db_path = BASE_DIR / "data" / "db" / "nifty100.db"
schema_path = BASE_DIR / "sql" / "schema.sql"

db_path.parent.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(db_path)

with open(schema_path, "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("Database created successfully!")