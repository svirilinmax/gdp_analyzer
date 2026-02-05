"""Базовый класс для отчетов."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseReport(ABC):
    """Абстрактный базовый класс для всех отчетов."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Имя отчета (используется в --report)."""
        pass

    @abstractmethod
    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Генерация данных отчета из сырых данных."""
        pass

    @abstractmethod
    def display(self, report_data: List[Dict[str, Any]]) -> None:
        """Отображение отчета в консоли."""
        pass
