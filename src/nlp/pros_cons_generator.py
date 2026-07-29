import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "output", "analysis_parsed.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "pros_cons_generated.csv")

df = pd.read_csv(INPUT_FILE)

results = []

for _, row in df.iterrows():

    company = row["ticker"]

    # ---------------- PROS ----------------
    if row["roe"] >= 20:
        results.append({
            "company_id": row["company_id"],
            "company": company,
            "type": "Pro",
            "text": "Strong Return on Equity indicates efficient capital utilization.",
            "confidence_pct": 95
        })

    if row["debt_equity"] <= 0.5:
        results.append({
            "company_id": row["company_id"],
            "company": company,
            "type": "Pro",
            "text": "Low Debt-to-Equity ratio indicates a healthy balance sheet.",
            "confidence_pct": 90
        })

    if row["current_ratio"] >= 1.5:
        results.append({
            "company_id": row["company_id"],
            "company": company,
            "type": "Pro",
            "text": "Strong liquidity position with good Current Ratio.",
            "confidence_pct": 88
        })

    # ---------------- CONS ----------------
    if row["roe"] < 15:
        results.append({
            "company_id": row["company_id"],
            "company": company,
            "type": "Con",
            "text": "Low ROE suggests weaker profitability.",
            "confidence_pct": 85
        })

    if row["debt_equity"] > 1:
        results.append({
            "company_id": row["company_id"],
            "company": company,
            "type": "Con",
            "text": "High Debt-to-Equity ratio increases financial risk.",
            "confidence_pct": 92
        })

    if row["current_ratio"] < 1:
        results.append({
            "company_id": row["company_id"],
            "company": company,
            "type": "Con",
            "text": "Weak liquidity position.",
            "confidence_pct": 84
        })

result_df = pd.DataFrame(results)

result_df.to_csv(OUTPUT_FILE, index=False)

print("✓ Generated:", OUTPUT_FILE)
print(result_df.head())