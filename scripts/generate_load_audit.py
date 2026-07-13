import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent

DB = BASE_DIR / "data" / "db" / "nifty100.db"
REPORT = BASE_DIR / "reports" / "load_audit.csv"

conn = sqlite3.connect(DB)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

records = []

for table in tables["name"]:

    count = pd.read_sql(
        f"SELECT COUNT(*) AS rows FROM {table}",
        conn
    ).iloc[0]["rows"]

    records.append({
        "table_name": table,
        "rows_loaded": count,
        "status": "SUCCESS",
        "timestamp": datetime.now()
    })

pd.DataFrame(records).to_csv(REPORT, index=False)

conn.close()

print("load_audit.csv generated successfully.")