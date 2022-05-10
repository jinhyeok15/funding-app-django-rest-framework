from enum import Enum


DEFAULT_CURRENCY = 'WON'


class Money(bytes, Enum):

    WON = (0, "Won", 10)

    def __new__(cls, name, cls_name, min_):
        obj = bytes.__new__(cls, [name])
        obj._value_ = name
        obj.cls_name = cls_name
        obj.min_ = min_
        return obj
    
    def __call__(self, value):
        if value<self.min_:
            raise ValueError
        self.__value = value
        return self
    
    def __str__(self):
        value = str(self.__value)
        string = ''
        cnt = 1
        for i in reversed(range(len(value))):
            string = value[i]+string
            if cnt==3:
                string = ','+string
            cnt += 1
        return string


def money(value):
    return Money[DEFAULT_CURRENCY](value)
