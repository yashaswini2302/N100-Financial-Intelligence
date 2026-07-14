import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios LIMIT 10",
    conn
)

print(df)

conn.close()