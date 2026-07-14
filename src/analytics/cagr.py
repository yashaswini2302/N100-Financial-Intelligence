import math


def calculate_cagr(start, end, years):
    """
    CAGR = ((End / Start) ** (1 / Years) - 1) * 100
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start == 0:
        return None, "ZERO_BASE"

    if start is None or end is None:
        return None, "INSUFFICIENT_DATA"

    if start < 0 and end < 0:
        return None, "BOTH_NEGATIVE"

    if start < 0 < end:
        return None, "TURNAROUND"

    if start > 0 > end:
        return None, "DECLINE_TO_LOSS"

    cagr = ((end / start) ** (1 / years) - 1) * 100

    return round(cagr, 2), "NORMAL"