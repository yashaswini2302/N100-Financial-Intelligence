import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

conn = sqlite3.connect("data/db/nifty100.db")

df = pd.read_sql("SELECT * FROM peer_percentiles", conn)

conn.close()

os.makedirs("output/radar_charts", exist_ok=True)

metrics = [
    "return_on_equity_pct_percentile",
    "return_on_assets_pct_percentile",
    "net_profit_margin_pct_percentile",
    "asset_turnover_percentile",
    "revenue_cagr_5yr_percentile",
]

for _, row in df.iterrows():

    values = [row[m] for m in metrics]

    values += values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(metrics),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))

    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values)

    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels([
        "ROE",
        "ROA",
        "NPM",
        "Asset Turnover",
        "Revenue CAGR"
    ])

    ax.set_title(f"Company {row['company_id']}")

    plt.savefig(
        f"output/radar_charts/company_{row['company_id']}.png"
    )

    plt.close()

print("Radar charts generated successfully.")