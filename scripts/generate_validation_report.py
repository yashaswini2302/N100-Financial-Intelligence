import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB = BASE_DIR / "data" / "db" / "nifty100.db"
REPORT = BASE_DIR / "reports" / "validation_failures.csv"

conn = sqlite3.connect(DB)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

issues = []

for table in tables["name"]:

    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    # Missing values
    for col in df.columns:
        missing = df[df[col].isnull()]
        for idx in missing.index:
            issues.append({
                "table_name": table,
                "row_number": idx,
                "column_name": col,
                "issue": "Missing Value",
                "severity": "HIGH"
            })

    # Duplicate rows
    duplicates = df[df.duplicated()]
    for idx in duplicates.index:
        issues.append({
            "table_name": table,
            "row_number": idx,
            "column_name": "-",
            "issue": "Duplicate Row",
            "severity": "MEDIUM"
        })

pd.DataFrame(
    issues,
    columns=[
        "table_name",
        "row_number",
        "column_name",
        "issue",
        "severity"
    ]
).to_csv(REPORT, index=False)

conn.close()

print("validation_failures.csv generated successfully.")