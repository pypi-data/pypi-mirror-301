from __future__ import annotations

from abc import ABC, abstractmethod


class QueryElementBase(ABC):
    def __init__(self, value: str):
        self._value = self.process_value(value)

    @abstractmethod
    def process_value(self, value: str) -> str:
        pass

    def __str__(self):
        return self._value

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value})"


class QueryIdentifier(QueryElementBase):
    def process_value(self, value: str):
        return f'"{value}"'


class QueryLiteral(QueryElementBase):
    def process_value(self, value: str):
        return value
