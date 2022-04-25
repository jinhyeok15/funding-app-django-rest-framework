from datetime import date


def _validate_date_string(str_date):
    try:
        date_value = date.fromisoformat(str_date)
        if date_value<date.today():
            raise ValueError
        return date_value
    except ValueError:
        raise ValueError


class DateComponent:
    def __init__(self, str_date):
        self.__str_date = str_date
        self.__date_value = _validate_date_string(str_date=str_date)
    
    def __str__(self) -> str:
        return self.__str_date
    
    def as_date(self):
        return self.__date_value    
