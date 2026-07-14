import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.analytics.cashflow_kpis import *


def test_free_cash_flow():
    assert free_cash_flow(500, -200) == 300


def test_quality_score():
    assert cfo_quality_score([100, 120], [80, 100]) == "High Quality"


def test_quality_zero_pat():
    assert cfo_quality_score([100], [0]) is None


def test_capex():
    assert capex_intensity(-100, 1000) == 10.0


def test_capex_zero_sales():
    assert capex_intensity(-100, 0) is None


def test_fcf_conversion():
    assert fcf_conversion_rate(200, 400) == 50.0


def test_fcf_conversion_zero():
    assert fcf_conversion_rate(200, 0) is None


def test_pattern():
    assert capital_allocation_pattern(100, -100, -50) == "Shareholder Returns"