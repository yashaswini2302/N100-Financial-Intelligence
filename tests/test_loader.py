import os

def test_raw_folder_exists():
    assert os.path.exists("data/raw")

def test_database_exists():
    assert os.path.exists("data/db/nifty100.db")

def test_reports_exist():
    assert os.path.exists("reports/load_audit.csv")
    assert os.path.exists("reports/validation_failures.csv")
    assert os.path.exists("reports/query_results.txt")