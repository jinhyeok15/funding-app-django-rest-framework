from datetime import date
from typing import Union


def _validate_date_string(str_date):
    try:
        date_value = date.fromisoformat(str_date)
        if date_value<date.today():
            raise ValueError
        return date_value
    except ValueError:
        raise ValueError


class DateComponent:
    def __init__(self, value: Union[str, date]):
        if isinstance(value, str):
            self.__str_date = value
            try:
                self.__date_value = date.fromisoformat(value)
            except ValueError:
                raise ValueError
        elif isinstance(value, date):
            self.__str_date = value.strftime('%Y-%m-%d')
            self.__date_value = value
    
    def __str__(self) -> str:
        return self.__str_date
    
    def as_date(self):
        return self.__date_value
    
    def get_d_day(self):
        return (self.as_date()-date.today()).days


class FinalDateComponent(DateComponent):
    def __init__(self, str_date):
        super().__init__(str_date)
        if self.as_date()<date.today():
            raise ValueError


def get_today():
    return DateComponent(date.today())
