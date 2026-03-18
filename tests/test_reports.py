from gdp_analyzer.reports.average_gdp import AverageGdpReport
from gdp_analyzer.reports.registry import ReportRegistry


def test_average_gdp_report_name():
    """Тест имени отчета."""

    report = AverageGdpReport()
    assert report.name == "average-gdp"


def test_average_gdp_report_generate():
    """Тест генерации отчета по среднему ВВП."""

    report = AverageGdpReport()

    test_data = [
        {"country": "USA", "gdp": "1000", "year": "2023"},
        {"country": "USA", "gdp": "900", "year": "2022"},
        {"country": "China", "gdp": "800", "year": "2023"},
        {"country": "China", "gdp": "700", "year": "2022"},
        {"country": "Russia", "gdp": "600", "year": "2023"},
        # Страна без ВВП
        {"country": "Germany", "year": "2023"},
        # Некорректный ВВП
        {"country": "France", "gdp": "invalid", "year": "2023"},
    ]

    result = report.generate(test_data)

    assert len(result) == 3
    assert result[0]["country"] == "USA"
    assert result[0]["average_gdp"] == 950.0
    assert result[1]["country"] == "China"
    assert result[1]["average_gdp"] == 750.0
    assert result[2]["country"] == "Russia"
    assert result[2]["average_gdp"] == 600.0


def test_average_gdp_report_generate_empty():
    """Тест генерации отчета из пустых данных."""

    report = AverageGdpReport()
    result = report.generate([])
    assert result == []


def test_report_registry():
    """Тест реестра отчетов."""

    # Проверяем, что отчет зарегистрирован
    report = ReportRegistry.get_report("average-gdp")
    assert report is not None
    assert report.name == "average-gdp"

    # Проверяем несуществующий отчет
    assert ReportRegistry.get_report("non-existent") is None

    # Проверяем список отчетов
    reports = ReportRegistry.list_reports()
    assert "average-gdp" in reports


def test_average_gdp_report_display_empty():
    """Тест отображения пустого отчета."""

    report = AverageGdpReport()
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        report.display([])
    output = f.getvalue()
    assert "Нет данных" in output


def test_average_gdp_inherits_from_base():
    """Проверяет, что AverageGdpReport наследуется от BaseReport."""
    from gdp_analyzer.reports.average_gdp import AverageGdpReport
    from gdp_analyzer.reports.base import BaseReport

    assert issubclass(AverageGdpReport, BaseReport)

    report = AverageGdpReport()
    assert hasattr(report, "name")
    assert hasattr(report, "generate")
    assert hasattr(report, "display")
