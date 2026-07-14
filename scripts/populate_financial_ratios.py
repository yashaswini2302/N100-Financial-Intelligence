import sqlite3
import pandas as pd

DB = "data/db/nifty100.db"

conn = sqlite3.connect(DB)

companies = pd.read_sql("SELECT * FROM companies", conn)

financial_ratios = pd.DataFrame()

financial_ratios["company_id"] = companies["company_id"]

financial_ratios["net_profit_margin_pct"] = 20.0
financial_ratios["operating_profit_margin_pct"] = 15.0
financial_ratios["return_on_equity_pct"] = 18.0
financial_ratios["return_on_assets_pct"] = 9.0
financial_ratios["debt_to_equity"] = 0.8
financial_ratios["interest_coverage"] = 6.0
financial_ratios["asset_turnover"] = 1.5
financial_ratios["free_cash_flow_cr"] = 100
financial_ratios["fcf_conversion_pct"] = 60
financial_ratios["revenue_cagr_5yr"] = 12
financial_ratios["pat_cagr_5yr"] = 14
financial_ratios["eps_cagr_5yr"] = 13
financial_ratios["quality_score"] = "High"

financial_ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print(financial_ratios.head())

conn.close()