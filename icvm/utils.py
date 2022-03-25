import decimal

def zero_safe_divide(numerator: decimal.Decimal, denominator: decimal.Decimal) -> decimal.Decimal:
    if denominator == 0:
        return 0
    else:
        return numerator / denominator