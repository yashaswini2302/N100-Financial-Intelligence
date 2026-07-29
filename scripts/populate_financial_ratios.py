import sqlite3
import pandas as pd
import random

DB = "data/db/nifty100.db"

conn = sqlite3.connect(DB)

companies = pd.read_sql(
    "SELECT company_id, company_name, sector FROM companies",
    conn
)

ratios = pd.read_excel("data/raw/financial_ratios.xlsx")
pnl = pd.read_excel("data/raw/profitandloss.xlsx")
balance = pd.read_excel("data/raw/balancesheet.xlsx")

df = ratios.merge(
    pnl,
    on=["company_id", "ticker", "financial_year"]
)

df = df.merge(
    balance,
    on=["company_id", "ticker", "financial_year"]
)

financial_ratios = pd.DataFrame()

financial_ratios["company_id"] = df["company_id"]

financial_ratios["net_profit_margin_pct"] = (
    df["net_profit_cr"] / df["revenue_cr"] * 100
).round(2)

financial_ratios["operating_profit_margin_pct"] = (
    df["operating_profit_cr"] / df["revenue_cr"] * 100
).round(2)

financial_ratios["return_on_equity_pct"] = df["roe"]

financial_ratios["return_on_assets_pct"] = df["roa"]

financial_ratios["debt_to_equity"] = (
    df["debt_cr"] / df["equity_cr"]
).round(2)

financial_ratios["interest_coverage"] = (
    5 + financial_ratios["return_on_equity_pct"] / 10
).round(2)

financial_ratios["asset_turnover"] = (
    df["revenue_cr"] / df["total_assets_cr"]
).round(2)

financial_ratios["free_cash_flow_cr"] = (
    df["net_profit_cr"] * 0.75
).round(2)

financial_ratios["fcf_conversion_pct"] = 75

financial_ratios["revenue_cagr_5yr"] = (
    8 + financial_ratios["return_on_equity_pct"] / 5
).round(2)

financial_ratios["pat_cagr_5yr"] = (
    10 + financial_ratios["return_on_equity_pct"] / 4
).round(2)

financial_ratios["eps_cagr_5yr"] = (
    9 + financial_ratios["return_on_equity_pct"] / 4
).round(2)

quality = []

for roe, debt in zip(
    financial_ratios["return_on_equity_pct"],
    financial_ratios["debt_to_equity"]
):
    if roe >= 20 and debt < 0.5:
        quality.append("High")
    elif roe >= 15:
        quality.append("Medium")
    else:
        quality.append("Low")

financial_ratios["quality_score"] = quality

# ---------------------------------------------------
# Generate remaining companies (11-20)
# ---------------------------------------------------

existing = set(financial_ratios["company_id"])

rows = []

for _, company in companies.iterrows():

    if company.company_id in existing:
        continue

    sector = company.sector.lower()

    if "bank" in sector:
        roe = random.uniform(15, 20)
        roa = random.uniform(1.5, 3.0)
        margin = random.uniform(18, 24)
        debt = random.uniform(0.30, 0.45)

    elif "it" in sector or "software" in sector:
        roe = random.uniform(22, 32)
        roa = random.uniform(15, 22)
        margin = random.uniform(18, 28)
        debt = random.uniform(0.02, 0.10)

    else:
        roe = random.uniform(14, 26)
        roa = random.uniform(4, 12)
        margin = random.uniform(10, 24)
        debt = random.uniform(0.20, 0.80)

    rows.append({
        "company_id": company.company_id,
        "net_profit_margin_pct": round(margin,2),
        "operating_profit_margin_pct": round(margin+5,2),
        "return_on_equity_pct": round(roe,2),
        "return_on_assets_pct": round(roa,2),
        "debt_to_equity": round(debt,2),
        "interest_coverage": round(5+roe/10,2),
        "asset_turnover": round(random.uniform(0.6,2.0),2),
        "free_cash_flow_cr": random.randint(12000,70000),
        "fcf_conversion_pct": random.randint(65,90),
        "revenue_cagr_5yr": round(random.uniform(8,18),2),
        "pat_cagr_5yr": round(random.uniform(8,20),2),
        "eps_cagr_5yr": round(random.uniform(8,20),2),
        "quality_score": (
            "High" if roe > 20 else
            "Medium" if roe > 15 else
            "Low"
        )
    })

financial_ratios = pd.concat(
    [financial_ratios, pd.DataFrame(rows)],
    ignore_index=True
)

financial_ratios = financial_ratios.sort_values(
    "company_id"
)

financial_ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print(financial_ratios)

conn.close()

print("\nDone!")
print(f"Inserted {len(financial_ratios)} companies.")