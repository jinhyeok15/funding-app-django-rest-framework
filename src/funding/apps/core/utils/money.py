from enum import Enum


DEFAULT_CURRENCY = 'WON'


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


class Money(bytes, Enum):

    WON = (0, "Won", 0, 9999999999)

    def __new__(cls, name, cls_name, min_, max_):
        obj = bytes.__new__(cls, [name])
        obj._value_ = name
        obj.cls_name = cls_name
        obj.min_ = min_
        obj.max_ = max_
        return obj
    
    def __call__(self, value):
        if isinstance(value, str):
            self.__value = _str_currency_to_int(value)
        else:
            self.__value = value
        if self.__value<self.min_ or self.__value>self.max_:
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
    
    def value_of(self, type):
        if type.__name__=='int':
            return self.__value
        if type.__name__=='str':
            return str(self)
        raise TypeError


def money(value):
    return Money[DEFAULT_CURRENCY](value)
