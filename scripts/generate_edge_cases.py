import sqlite3

conn = sqlite3.connect("data/db/nifty100.db")
cursor = conn.cursor()

cursor.execute("""
SELECT company_id,
       debt_to_equity,
       return_on_equity_pct,
       revenue_cagr_5yr
FROM financial_ratios
""")

rows = cursor.fetchall()

with open("output/ratio_edge_cases.log", "w") as f:
    for row in rows:
        company, de, roe, cagr = row

        if de is not None and de > 5:
            f.write(f"Company {company}: High Debt-to-Equity ({de})\n")

        if roe is not None and roe < 0:
            f.write(f"Company {company}: Negative ROE ({roe})\n")

        if cagr is None:
            f.write(f"Company {company}: Missing Revenue CAGR\n")

print("ratio_edge_cases.log generated successfully.")

conn.close()