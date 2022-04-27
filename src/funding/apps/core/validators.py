from .exceptions import *
from .components import date

def validate_final_date_component(value):
    try:
        date_cmp = date.FinalDateComponent(value)
    except ValueError:
        raise FinalDateValidationError(value)
