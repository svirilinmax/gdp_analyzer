"""Отчет по среднему ВВП по странам."""

from collections import defaultdict
from typing import Any, Dict, List

from tabulate import tabulate

from .base import BaseReport


class AverageGdpReport(BaseReport):
    """Отчет со средним ВВП по странам."""

    @property
    def name(self) -> str:
        return "average-gdp"

    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Генерация отчета со средним ВВП по странам.

        Args:
            data: Список словарей с данными

        Returns:
            Отсортированный список словарей с country и average_gdp
        """
        # Группировка данных по странам
        gdp_by_country = defaultdict(list)

        for row in data:
            # Обработка ключей в разных регистрах
            row_lower = {k.lower(): v for k, v in row.items()}
            country = row_lower.get("country")
            gdp_value = row_lower.get("gdp")

            if country and gdp_value:
                try:
                    gdp = float(gdp_value)
                    gdp_by_country[country].append(gdp)
                except (ValueError, TypeError):
                    # Пропускаем некорректные значения
                    continue

        # Расчет среднего ВВП для каждой страны
        report_data = []
        for country, gdp_values in gdp_by_country.items():
            if gdp_values:
                avg_gdp = sum(gdp_values) / len(gdp_values)
                report_data.append(
                    {"country": country, "average_gdp": round(avg_gdp, 2)}
                )

        # Сортировка по убыванию ВВП
        report_data.sort(key=lambda x: x["average_gdp"], reverse=True)

        return report_data

    def display(self, report_data: List[Dict[str, Any]]) -> None:
        """
        Отображение отчета в виде таблицы.

        Args:
            report_data: Данные для отображения
        """
        if not report_data:
            print("Нет данных для отображения")
            return

        # Подготавливаем данные для таблицы с нумерацией
        table_data = []
        for i, row in enumerate(report_data, 1):
            table_data.append([i, row["country"], f"{row['average_gdp']:.2f}"])

        headers = ["", "country", "gdp"]

        print(
            tabulate(
                table_data,
                headers=headers,
                tablefmt="simple_grid",
                stralign="center",
                numalign="right",
                floatfmt=".2f",
                colalign=("right", "left", "right"),
            )
        )
