from src.wallets.exceptions import NotComparisonException, NegativeValueException
from src.wallets import currency
import math


class Money:
    __slots__ = ("__currency", "__value")
    
    def __init__(self, value: int, currency: str):
        if value < 0 or value == math.inf:
            raise NegativeValueException
        
        self.__currency: str = currency
        self.__value: int = value
    

    @property
    def value(self) -> int:
        """
            Значение
        """
        
        return self.__value


    @property
    def currency(self) -> str:
        """
            Валюта
        """
        
        return self.__currency


    def __add__(self, other: Money|int) -> Money:
        """
            Сложение / вложение денег той же валюты или целого числа
        """
        
        # if other type is Money class
        if isinstance(other, Money):
            if other.value < 0:
                raise NegativeValueException
            if other.currency != self.currency:
                raise NotComparisonException
        else:
            # if other type is int
            if other > 0:
                raise NegativeValueException

        self.__value += other.value
        return self


    def __sub__(self, other: Money|int) -> Money:
        """
            Вычитание / снятие денег той же валюты или целого числа
        """
        
        # if other type is Money class
        if isinstance(other, Money):
            if self.value - other.value < 0 and other.value > 0:
                raise NegativeValueException
            if other.currency != self.currency:
                raise NotComparisonException

        if other.value > 0:
            pass

        self.__value -= other.value
        return self


    def __eq__(self, other: Money) -> bool:
        """
            Оператор сравнения

            input:
                - other: type Money
            output:
                - true: равно кол-во денег и валюта
                - false: не равно кол-во денег и валюта
        """
        
        
        return self.currency == other.currency and self.value == other.value



class Wallet:
    
    def __init__(self, money: Money):
        self.__d: dict[Money] = {}
        self.__d[money.currency] = money

    @property
    def currencies(self) -> list[str]:
        """
            Получение списка хранимой валюты
        """
        return self.__d.keys()
    
        
    def __getitem__(self, key: str) -> Money:
        """
            Получение объекта по валюте
        """
        return self.__d[key] if key in self.__d else Money(value=0, currency=key)


    def __delitem__(self, key) -> None:
        if key not in self.__d: return
        del self.__d[key]
    

    def __len__(self) -> int:
        """
            Получение размера списка хранимой валюты
        """
                
        return len(self.currencies)

    
    def __contains__(self, item) -> bool:
        return item in self.__d

    
    def sub(self, money: Money) -> Wallet:
        if money.currency not in self.__d:
            self.__d[money.currency] = money
        self.__d[money.currency] -= money
        return self

    
    def add(self, money: Money) -> Wallet:
        if money.currency not in self.__d:
            self.__d[money.currency] = money
        self.__d[money.currency] += money
        return self