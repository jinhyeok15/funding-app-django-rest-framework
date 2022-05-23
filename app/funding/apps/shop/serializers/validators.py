from funding.apps.core.utils.components import date
from funding.apps.core.exceptions import (
    TargetAmountBoundException,
    FinalDateValidationError
)


def validate_target_amount(value):
    if value < 10000:
        raise TargetAmountBoundException(value)
    return value


def validate_final_date(value):
    compare_num = date.DateComponent(value).compare_of(date.get_today())
    if compare_num != 1:
        raise FinalDateValidationError(value)
    return value
