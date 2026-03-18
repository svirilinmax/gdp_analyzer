from typing import Dict, Optional

from .average_gdp import AverageGdpReport
from .base import BaseReport
from .median_coffee import MedianCoffeeReport


class ReportRegistry:
    """Реестр для управления доступными отчетами."""

    _reports: Dict[str, BaseReport] = {}

    @classmethod
    def register_report(cls, report: BaseReport) -> None:
        """Регистрация нового отчета."""
        cls._reports[report.name] = report

    @classmethod
    def get_report(cls, report_name: str) -> Optional[BaseReport]:
        """Получение отчета по имени."""
        return cls._reports.get(report_name)

    @classmethod
    def list_reports(cls) -> list:
        """Список доступных отчетов."""
        return list(cls._reports.keys())


# Регистрация стандартных отчетов
ReportRegistry.register_report(AverageGdpReport())
ReportRegistry.register_report(MedianCoffeeReport())
