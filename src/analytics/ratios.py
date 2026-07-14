import numpy as np


# -------------------------
# Profitability Ratios
# -------------------------

def net_profit_margin(net_profit, sales):
    if sales == 0 or sales is None:
        return None
    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    if sales == 0 or sales is None:
        return None
    return round((operating_profit / sales) * 100, 2)


def return_on_equity(net_profit, equity):
    if equity == 0 or equity is None:
        return None
    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(ebit, equity, borrowings):
    capital = equity + borrowings
    if capital == 0:
        return None
    return round((ebit / capital) * 100, 2)


def return_on_assets(net_profit, total_assets):
    if total_assets == 0 or total_assets is None:
        return None
    return round((net_profit / total_assets) * 100, 2)


# -------------------------
# Leverage Ratios
# -------------------------

def debt_to_equity(borrowings, equity):
    if borrowings == 0:
        return 0

    if equity == 0 or equity is None:
        return None

    return round(borrowings / equity, 2)


def interest_coverage_ratio(operating_profit, other_income, interest):
    if interest == 0 or interest is None:
        return None

    return round((operating_profit + other_income) / interest, 2)


def net_debt(borrowings, investments):
    return borrowings - investments


# -------------------------
# Efficiency Ratios
# -------------------------

def asset_turnover(sales, total_assets):
    if total_assets == 0 or total_assets is None:
        return None

    return round(sales / total_assets, 2)