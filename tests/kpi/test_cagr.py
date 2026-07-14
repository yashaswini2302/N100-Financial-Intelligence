import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.analytics.cagr import calculate_cagr


def test_normal_cagr():
    value, flag = calculate_cagr(100, 200, 5)
    assert flag == "NORMAL"


def test_turnaround():
    value, flag = calculate_cagr(-100, 200, 5)
    assert flag == "TURNAROUND"


def test_decline():
    value, flag = calculate_cagr(100, -50, 5)
    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():
    value, flag = calculate_cagr(-100, -200, 5)
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():
    value, flag = calculate_cagr(0, 200, 5)
    assert flag == "ZERO_BASE"


def test_invalid_years():
    value, flag = calculate_cagr(100, 200, 0)
    assert flag == "INVALID_YEARS"


def test_insufficient_data():
    value, flag = calculate_cagr(None, None, 5)
    assert flag == "INSUFFICIENT_DATA"