import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "db" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

print("\nDATA QUALITY REPORT")
print("=" * 50)

for table in tables["name"]:

    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    print(f"\nTable: {table}")
    print(f"Rows : {len(df)}")

    missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    print(f"Missing Values : {missing}")
    print(f"Duplicate Rows : {duplicates}")

conn.close()