import abc


class ComponentBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def compare_of(self, a):
        ...
    
    @abc.abstractmethod
    def value_of(self, _type_):
        ...
