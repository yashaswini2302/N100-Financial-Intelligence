import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
companies = pd.read_sql(
    "SELECT company_id, company_name, sector FROM companies",
    conn
)

conn.close()

# Merge company information
df = ratios.merge(companies, on="company_id", how="left")

metrics = [
    "return_on_equity_pct",
    "return_on_assets_pct",
    "net_profit_margin_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "eps_cagr_5yr",
    "interest_coverage",
    "asset_turnover",
]

for metric in metrics:
    ascending = metric == "debt_to_equity"

    df[f"{metric}_percentile"] = (
        df.groupby("sector")[metric]
          .rank(pct=True, ascending=ascending)
          .round(3)
    )

print(df.head())

conn = sqlite3.connect("data/db/nifty100.db")

df.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("\npeer_percentiles table created successfully.")