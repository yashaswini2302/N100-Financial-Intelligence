import sqlite3
import pandas as pd

conn = sqlite3.connect("data/db/nifty100.db")
df = pd.read_sql("SELECT * FROM financial_ratios", conn)
conn.close()


def quality(df):
    return df[
        (df["return_on_equity_pct"] >= 15)
        & (df["debt_to_equity"] <= 1)
    ]


def value(df):
    return df[df["debt_to_equity"] <= 2]


def growth(df):
    return df[df["revenue_cagr_5yr"] >= 15]


def dividend(df):
    return df[df["free_cash_flow_cr"] > 0]


def debt_free(df):
    return df[df["debt_to_equity"] == 0]


def turnaround(df):
    return df[df["revenue_cagr_5yr"] > 10]


print("=" * 50)
print(" N100 FINANCIAL SCREENER")
print("=" * 50)

print("1. Quality Compounder")
print("2. Value Pick")
print("3. Growth Accelerator")
print("4. Dividend Champion")
print("5. Debt Free")
print("6. Turnaround")

choice = input("\nEnter your choice (1-6): ")

mapping = {
    "1": quality,
    "2": value,
    "3": growth,
    "4": dividend,
    "5": debt_free,
    "6": turnaround,
}

if choice not in mapping:
    print("Invalid choice.")
else:
    result = mapping[choice](df)

    print("\nCompanies Found:", len(result))
    print(result.head())

    result.to_excel(
        "output/exports/selected_screen.xlsx",
        index=False
    )

    print("\nSaved to output/exports/selected_screen.xlsx")