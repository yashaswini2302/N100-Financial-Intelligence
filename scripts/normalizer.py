import pandas as pd

def normalize_year(df):
    """
    Convert year columns to integer.
    """

    year_columns = [
        "year",
        "founded_year",
        "financial_year"
    ]

    for col in year_columns:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .fillna(0)
                .astype(int)
            )

    return df


def normalize_ticker(df):
    """
    Clean ticker symbols.
    """

    if "ticker" in df.columns:
        df["ticker"] = (
            df["ticker"]
            .astype(str)
            .str.upper()
            .str.strip()
        )

    return df