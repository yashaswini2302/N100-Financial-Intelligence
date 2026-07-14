import os

def test_reports():
    assert os.path.exists("reports/sprint1_summary.txt")
    assert os.path.exists("reports/sprint2_summary.txt")
    assert os.path.exists("reports/sprint3_summary.txt")

def test_database():
    assert os.path.exists("data/db/nifty100.db")

def test_exports():
    assert os.path.exists("output/exports/screener_results.csv")
    assert os.path.exists("output/exports/screener_results.xlsx")
    assert os.path.exists("output/exports/screener_results.json")

def test_radar_folder():
    assert os.path.exists("output/radar_charts")

def test_cli():
    assert os.path.exists("src/screener/cli.py")