from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Order:
    order_id: str
    items_total: float
    customer_id: str
    loyalty_points: int


class Discount(ABC):
    @abstractmethod
    def is_applicable(self, order: Order) -> bool:
        """Проверяет, можно ли применить эту скидку к данному заказу"""
        ...

    @abstractmethod
    def calculate(self, order: Order) -> float:
        """Рассчитывает сумму скидки"""
        ...


class FixedDiscount(Discount):
    def __init__(self, threshold: float, discount_amount: float):
        self.threshold = threshold
        self.discount_amount = discount_amount

    def is_applicable(self, order: Order) -> bool:
        return order.items_total >= self.threshold

    def calculate(self, order: Order) -> float:
        return self.discount_amount


class FixedDiscount(Discount):
    def __init__(self, threshold: float, discount_amount: float):
        self.threshold = threshold
        self.discount_amount = discount_amount

    def is_applicable(self, order: Order) -> bool:
        return order.items_total >= self.threshold

    def calculate(self, order: Order) -> float:
        return self.discount_amount



class LoyaltyDiscount(Discount):
    def __init__(self, points_threshold: int, discount_amount: float):
        self.points_threshold = points_threshold
        self.discount_amount = discount_amount

    def is_applicable(self, order: Order) -> bool:
        return order.loyalty_points >= self.points_threshold

    def calculate(self, order: Order) -> float:
        return self.discount_amount



class DiscountEngine:
    def __init__(self):
        self.discounts: list[Discount] = []

    def register_discount(self, discount: Discount) -> None:
        """Добавляет скидку в систему"""
        self.discounts.append(discount)

    def get_applicable_discounts(self, order: Order) -> list[Discount]:
        """Возвращает список скидок, применимых к заказу"""
        return [d for d in self.discounts if d.is_applicable(order)]

    def apply_discounts(self, order: Order) -> float:
        """
        Применяет все подходящие скидки и возвращает итоговую сумму.
        Скидки применяются последовательно: каждая следующая
        применяется к уже уменьшенной сумме.
        """
        total = order.items_total
        for discount in self.get_applicable_discounts(order):
            discount_amount = discount.calculate(order)
            total -= discount_amount
        return max(total, 0)