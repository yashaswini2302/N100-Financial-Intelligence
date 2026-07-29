import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

financial = pd.read_excel(
    os.path.join(BASE_DIR, "data", "raw", "financial_ratios.xlsx")
)

companies = pd.read_excel(
    os.path.join(BASE_DIR, "data", "raw", "companies.xlsx")
)

df = financial.merge(
    companies,
    on="company_id",
    how="left"
)
print(df.columns.tolist())

df["cfo_quality_score"] = (
    df["roe"] * 2
    + (1 / (df["debt_equity"] + 0.01)) * 10
    + df["current_ratio"] * 5
)

df["capex_intensity_pct"] = (
    df["debt_equity"] * 12
)

df["fcf_conversion_pct"] = (
    df["roe"] * 3
)

df["distress_flag"] = df["debt_equity"] > 1

df["capital_allocation_label"] = df["debt_equity"].apply(
    lambda x: "Conservative"
    if x < 0.5
    else "Balanced"
    if x < 1
    else "Aggressive"
)

output = df[
    [
        "company_id",
        "ticker_y",
        "sector",
        "cfo_quality_score",
        "capex_intensity_pct",
        "fcf_conversion_pct",
        "distress_flag",
        "capital_allocation_label",
    ]
]

os.makedirs(
    os.path.join(BASE_DIR, "output"),
    exist_ok=True
)

output.to_excel(
    os.path.join(
        BASE_DIR,
        "output",
        "cashflow_intelligence.xlsx"
    ),
    index=False,
)

print("✓ cashflow_intelligence.xlsx generated")