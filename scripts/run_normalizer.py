import pandas as pd
from pathlib import Path

from normalizer import normalize_year, normalize_ticker

RAW = Path("data/raw")
PROCESSED = Path("data/processed")

PROCESSED.mkdir(exist_ok=True)

for file in RAW.glob("*.xlsx"):

    df = pd.read_excel(file)

    df = normalize_year(df)
    df = normalize_ticker(df)

    output = PROCESSED / file.name

    df.to_excel(output, index=False)

    print(f"Processed {file.name}")

print("Normalization Complete!")