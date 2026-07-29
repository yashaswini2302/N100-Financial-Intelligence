import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

df = pd.read_excel(
    os.path.join(
        BASE_DIR,
        "output",
        "cashflow_intelligence.xlsx"
    )
)

summary = (
    df.groupby("capital_allocation_label")
      .size()
      .reset_index(name="company_count")
)

os.makedirs(
    os.path.join(BASE_DIR, "output"),
    exist_ok=True
)

summary.to_csv(
    os.path.join(
        BASE_DIR,
        "output",
        "capital_allocation.csv"
    ),
    index=False
)

print(summary)

print("\n✓ capital_allocation.csv generated")