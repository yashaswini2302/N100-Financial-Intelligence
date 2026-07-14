import os

def test_ratio_file_exists():
    assert os.path.exists("src/analytics/ratios.py")

def test_cagr_file_exists():
    assert os.path.exists("src/analytics/cagr.py")

def test_cashflow_file_exists():
    assert os.path.exists("src/analytics/cashflow_kpis.py")

def test_financial_ratio_table_exists():
    assert os.path.exists("data/db/nifty100.db")

def test_edge_case_log_exists():
    assert os.path.exists("output/ratio_edge_cases.log")