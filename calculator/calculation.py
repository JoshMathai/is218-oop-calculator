from abc import ABC, abstractmethod
from collections.abc import Callable


class Calculation(ABC):
    def __init__(self, a: float, b: float,
                 operation: Callable[[float, float], float]):
        # Each calculation owns its two numbers and chosen operation.
        self.a = a
        self.b = b
        self.operation = operation

    @classmethod
    def create(cls, a, b, operation):
        # cls is the concrete class that called create().
        # The factory builds a new object of that class.
        return cls(a, b, operation)

    @abstractmethod
    def execute(self) -> float:  # pragma: no cover
        # This is the promise; concrete classes supply the real work.
        # execute() replaces get_result() and returns the answer.
        pass


class ArithmeticCalculation(Calculation):
    def execute(self) -> float:
        # An instance method uses this calculation's stored values.
        return self.operation(self.a, self.b)