import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

df = pd.read_sql("SELECT * FROM financial_ratios", conn)

conn.close()

df["composite_score"] = (
    0.35 * df["return_on_equity_pct"]
    + 0.30 * df["free_cash_flow_cr"]
    + 0.20 * df["revenue_cagr_5yr"]
    + 0.15 * (100 - df["debt_to_equity"] * 10)
)

df = df.sort_values("composite_score", ascending=False)

print(df[["company_id", "composite_score"]].head())

df.to_excel("output/screener_output.xlsx", index=False)

print("\nCreated output/screener_output.xlsx")