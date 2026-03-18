from collections import defaultdict
from statistics import median
from typing import Any, Dict, List

from tabulate import tabulate

from .base import BaseReport


class MedianCoffeeReport(BaseReport):
    """Отчет с медианными тратами на кофе по каждому студенту."""

    @property
    def name(self) -> str:
        return "median-coffee"

    def generate(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Генерация отчета с медианными тратами на кофе по студентам.
        """
        coffee_by_student = defaultdict(list)

        for row in data:
            row_lower = {k.lower(): v for k, v in row.items()}
            student = None
            for key in ["student", "студент"]:
                if key in row_lower:
                    student = row_lower[key]
                    break

            coffee_value = row_lower.get("coffee_spent")

            if student and coffee_value:
                try:
                    coffee = float(coffee_value)
                    coffee_by_student[student].append(coffee)
                except (ValueError, TypeError):
                    continue

        report_data = []
        for student, coffee_values in coffee_by_student.items():
            if coffee_values:
                median_coffee = median(coffee_values)
                report_data.append(
                    {"student": student, "median_coffee": round(median_coffee, 2)}
                )

        report_data.sort(key=lambda x: x["median_coffee"], reverse=True)

        return report_data

    def display(self, report_data: List[Dict[str, Any]]) -> None:
        """
        Отображение отчета в виде таблицы.
        """
        if not report_data:
            print("Нет данных для отображения")
            return

        table_data = []
        for i, row in enumerate(report_data, 1):
            table_data.append([i, row["student"], f"{row['median_coffee']:.2f}"])

        headers = ["", "Студент", "Медианные траты на кофе"]

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
