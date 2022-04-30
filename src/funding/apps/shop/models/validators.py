from funding.apps.core.exceptions import (
    # models validation error
    FinalDateValidationError
)
from funding.apps.core.components import date


# models validation
def validate_final_date_component(value):
    try:
        date_cmp = date.FinalDateComponent(value)
    except ValueError:
        raise FinalDateValidationError(value)
