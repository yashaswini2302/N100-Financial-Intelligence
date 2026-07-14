def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow = Operating Activity + Investing Activity
    (Investing activity is usually negative)
    """
    return operating_activity + investing_activity


def cfo_quality_score(cfo_list, pat_list):
    """
    Average CFO/PAT ratio
    """

    ratios = []

    for cfo, pat in zip(cfo_list, pat_list):
        if pat == 0:
            return None

        ratios.append(cfo / pat)

    avg = sum(ratios) / len(ratios)

    if avg > 1:
        return "High Quality"

    elif avg >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"


def capex_intensity(capex, sales):
    if sales == 0:
        return None

    return round(abs(capex) / sales * 100, 2)


def fcf_conversion_rate(fcf, operating_profit):
    if operating_profit == 0:
        return None

    return round(fcf / operating_profit * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff):

    signs = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    mapping = {
        ("+", "-", "-"): "Shareholder Returns",
        ("+", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "-"): "Liquidating Assets",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "+", "-"): "Mixed"
    }

    return mapping.get(signs, "Mixed")