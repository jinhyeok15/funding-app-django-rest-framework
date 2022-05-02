from funding.apps.core.exceptions import (
    # models validation error
    FinalDateValidationError
)
from funding.apps.core.components import date


# models validation
def validate_final_date_component(value):
    compare_num = date.DateComponent(value).compare_of(date.get_today())
    if compare_num != 1:
        raise FinalDateValidationError(value)
