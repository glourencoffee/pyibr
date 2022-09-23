import decimal
import typing

__all__ = [
    'zero_safe_divide',
    'none_safe_divide'
]

def zero_safe_divide(numerator: decimal.Decimal, denominator: decimal.Decimal) -> decimal.Decimal:
    if denominator == 0:
        return 0
    else:
        return numerator / denominator

def none_safe_divide(numerator: typing.Optional[decimal.Decimal],
                     denominator: typing.Optional[decimal.Decimal]
) -> typing.Optional[decimal.Decimal]:

    if numerator is None or denominator is None:
        return None
    else:
        return zero_safe_divide(numerator, denominator)