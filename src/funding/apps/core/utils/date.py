from datetime import date
from typing import Union


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
        else:
            raise TypeError('value is not valid type')
    
    def __str__(self) -> str:
        return self.__str_date
    
    def as_date(self):
        return self.__date_value
    
    def get_d_day(self):
        return (self.as_date()-date.today()).days

    def compare_of(self, a):
        """
        obj.compare_of(a):
        if obj > a -> 1
        if obj == a -> 0
        if obj < a -> -1
        """
        if self.as_date() > a.as_date():
            return 1
        elif self.as_date() == a.as_date():
            return 0
        elif self.as_date() < a.as_date():
            return -1
        else:
            raise ValueError


def get_today():
    return DateComponent(date.today())
