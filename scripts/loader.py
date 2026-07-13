import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FOLDER = BASE_DIR / "data" / "raw"


def load_all_excel_files():
    datasets = {}

    excel_files = list(RAW_FOLDER.glob("*.xlsx"))

    if not excel_files:
        print("No Excel files found.")
        return datasets

    for file in excel_files:
        try:
            xls = pd.ExcelFile(file)

            for sheet in xls.sheet_names:
                df = pd.read_excel(file, sheet_name=sheet)

                key = f"{file.stem}_{sheet}"

                datasets[key] = df

                print(f"Loaded: {file.name} | Sheet: {sheet}")

        except Exception as e:
            print(f"Error loading {file.name}: {e}")

    return datasets


if __name__ == "__main__":
    data = load_all_excel_files()

    print("\nFiles Loaded:", len(data))