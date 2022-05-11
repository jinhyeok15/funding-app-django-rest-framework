from funding.apps.core.exceptions import (
    TargetAmountBoundException
)


def validate_target_amount(value):
    if value < 10000:
        raise TargetAmountBoundException(value)
    return value
