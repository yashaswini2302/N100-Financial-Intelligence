import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.analytics.ratios import *


# ---------- Day 08 ----------

def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.0


def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None


def test_operating_profit_margin():
    assert operating_profit_margin(150, 1000) == 15.0


def test_roe():
    assert return_on_equity(200, 500) == 40.0


def test_roe_zero_equity():
    assert return_on_equity(200, 0) is None


def test_roce():
    assert return_on_capital_employed(300, 500, 500) == 30.0


def test_roa():
    assert return_on_assets(100, 1000) == 10.0


def test_roa_zero_assets():
    assert return_on_assets(100, 0) is None


# ---------- Day 09 ----------

def test_debt_to_equity():
    assert debt_to_equity(500, 250) == 2.0


def test_zero_borrowings():
    assert debt_to_equity(0, 100) == 0


def test_interest_coverage():
    assert interest_coverage_ratio(500, 100, 100) == 6.0


def test_interest_zero():
    assert interest_coverage_ratio(500, 100, 0) is None


def test_net_debt():
    assert net_debt(1000, 300) == 700


def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.0


def test_asset_turnover_zero():
    assert asset_turnover(1000, 0) is None