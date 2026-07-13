import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "db" / "nifty100.db"
PROCESSED = BASE_DIR / "data" / "processed"

conn = sqlite3.connect(DB_PATH)

loaded = 0

for file in PROCESSED.glob("*.xlsx"):

    table = file.stem.lower()

    df = pd.read_excel(file)

    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {table}")

    loaded += 1

conn.close()

print(f"\nTotal tables loaded: {loaded}")
