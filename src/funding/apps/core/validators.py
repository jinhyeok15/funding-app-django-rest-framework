from django.core.exceptions import ValidationError
from .components import date

def validate_date_component(value):
    try:
        date_cmp = date.DateComponent(value)
    except ValueError:
        raise ValidationError(f"date 타입에 맞지 않습니다: {value}")
