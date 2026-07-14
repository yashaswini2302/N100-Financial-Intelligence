import sqlite3
import pandas as pd
import os

# Create output folder
os.makedirs("output/exports", exist_ok=True)

# Connect to database
conn = sqlite3.connect("data/db/nifty100.db")

# Load screener data
df = pd.read_sql("SELECT * FROM peer_percentiles", conn)

conn.close()

# Export to CSV
df.to_csv(
    "output/exports/screener_results.csv",
    index=False
)

# Export to Excel
df.to_excel(
    "output/exports/screener_results.xlsx",
    index=False
)

# Export to JSON
df.to_json(
    "output/exports/screener_results.json",
    orient="records",
    indent=4
)

print("Exports generated successfully!")

print("\nFiles Created:")
print("- output/exports/screener_results.csv")
print("- output/exports/screener_results.xlsx")
print("- output/exports/screener_results.json")