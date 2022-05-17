from .base import ComponentBase


DEFAULT_CURRENCY_TYPE = 'WON'


def _str_currency_to_int(str_curr):
    try:
        devided = str_curr.split(',')
        if not (1<=len(devided[0]) and len(devided[0])<=3):
            raise ValueError
        for i in range(1, len(devided)):
            if not len(devided[i]):
                raise ValueError
        return int(''.join(str_curr.split(',')))
    except ValueError:
        raise


class Money(ComponentBase):

    currency_data = {
        'WON': {
            'MIN': 0,
            'MAX': 9999999999
        }
    }

    def __init__(self, value=None, currency_type=DEFAULT_CURRENCY_TYPE):
        self.currency = self.currency_data[currency_type]
        self.MIN = self.currency['MIN']
        self.MAX = self.currency['MAX']
        self.__value = value
    
    def __call__(self, value):
        if isinstance(value, str):
            self.__value = _str_currency_to_int(value)
        else:
            self.__value = value
        if self.__value<self.MIN or self.__value>self.MAX:
            raise ValueError
        return self
    
    def __str__(self):
        strvalue = str(self.__value)
        string = ''
        cnt = 1
        for i in reversed(range(len(strvalue))):
            string = strvalue[i]+string
            if cnt==3:
                string = ','+string
            cnt += 1
        return string
    
    def times(self, num):
        return self(self.__value*num)
    
    def value_of(self, _type_):
        if _type_.__name__=='int':
            return self.__value
        if _type_.__name__=='str':
            return str(self)
        raise TypeError
    
    def compare_of(self, a):
        if self.__value > a.value_of(int):
            return 1
        elif self.__value < a.value_of(int):
            return -1
        elif self.__value == a.value_of(int):
            return 0
        else:
            raise ValueError


def money(value):
    return Money(DEFAULT_CURRENCY_TYPE)(value)
