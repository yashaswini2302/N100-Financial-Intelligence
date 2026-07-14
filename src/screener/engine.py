import sqlite3
import pandas as pd
import yaml


def load_config():
    with open("config/screener_config.yaml", "r") as f:
        return yaml.safe_load(f)


def load_ratios():
    conn = sqlite3.connect("data/db/nifty100.db")
    df = pd.read_sql("SELECT * FROM financial_ratios", conn)
    conn.close()
    return df


def quality_compounder(df):
    return df[
        (df["return_on_equity_pct"] >= 15)
        & (df["debt_to_equity"] <= 1)
        & (df["free_cash_flow_cr"] > 0)
        & (df["revenue_cagr_5yr"] >= 10)
    ]


def value_pick(df):
    return df[df["debt_to_equity"] <= 2]


def growth_accelerator(df):
    return df[
        (df["pat_cagr_5yr"] >= 20)
        & (df["revenue_cagr_5yr"] >= 15)
    ]


def dividend_champion(df):
    return df[df["free_cash_flow_cr"] > 0]


def debt_free(df):
    return df[df["debt_to_equity"] == 0]


def turnaround(df):
    return df[df["revenue_cagr_5yr"] > 10]


if __name__ == "__main__":

    df = load_ratios()

    print("\nQuality Compounder")
    print(quality_compounder(df).head())

    print("\nValue Pick")
    print(value_pick(df).head())

    print("\nGrowth Accelerator")
    print(growth_accelerator(df).head())

    print("\nDividend Champion")
    print(dividend_champion(df).head())

    print("\nDebt Free")
    print(debt_free(df).head())

    print("\nTurnaround")
    print(turnaround(df).head())