import os
import pandas as pd

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

INPUT_FILE = os.path.join(BASE_DIR, "data", "raw", "financial_ratios.xlsx")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "analysis_parsed.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read Excel
df = pd.read_excel(INPUT_FILE)

# Rename columns if needed
df.columns = [c.strip().lower() for c in df.columns]

# Save parsed output
df.to_csv(OUTPUT_FILE, index=False)

print(f"✓ Parsed file saved to:\n{OUTPUT_FILE}")
print(df.head())