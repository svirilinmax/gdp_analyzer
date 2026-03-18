from gdp_analyzer.reports.median_coffee import MedianCoffeeReport


def test_median_coffee_report_name():
    """Проверяет, что отчет имеет правильное имя."""
    report = MedianCoffeeReport()
    assert report.name == "median-coffee"


def test_median_coffee_generate_single_student():
    """Проверяет расчет медианы для одного студента."""
    report = MedianCoffeeReport()
    data = [
        {"student": "Иван Петров", "coffee_spent": "100"},
        {"student": "Иван Петров", "coffee_spent": "200"},
        {"student": "Иван Петров", "coffee_spent": "300"},
    ]

    result = report.generate(data)

    assert len(result) == 1
    assert result[0]["student"] == "Иван Петров"
    assert result[0]["median_coffee"] == 200.0  # медиана 100,200,300 = 200


def test_median_coffee_generate_multiple_students():
    """Проверяет расчет медианы для нескольких студентов."""
    report = MedianCoffeeReport()
    data = [
        # Иван - 3 значения
        {"student": "Иван", "coffee_spent": "100"},
        {"student": "Иван", "coffee_spent": "200"},
        {"student": "Иван", "coffee_spent": "300"},
        # Петр - 4 значения (четное количество)
        {"student": "Петр", "coffee_spent": "400"},
        {"student": "Петр", "coffee_spent": "500"},
        {"student": "Петр", "coffee_spent": "600"},
        {"student": "Петр", "coffee_spent": "700"},
    ]

    result = report.generate(data)

    assert len(result) == 2
    # Проверяем сортировку по убыванию
    assert result[0]["student"] == "Петр"  # медиана 550
    assert result[0]["median_coffee"] == 550.0
    assert result[1]["student"] == "Иван"  # медиана 200
    assert result[1]["median_coffee"] == 200.0


def test_median_coffee_generate_even_number():
    """Проверяет расчет медианы для четного количества значений."""
    report = MedianCoffeeReport()
    data = [
        {"student": "Анна", "coffee_spent": "10"},
        {"student": "Анна", "coffee_spent": "20"},
        {"student": "Анна", "coffee_spent": "30"},
        {"student": "Анна", "coffee_spent": "40"},
    ]

    result = report.generate(data)

    # Медиана для 10,20,30,40 = (20+30)/2 = 25
    assert result[0]["median_coffee"] == 25.0


def test_median_coffee_generate_with_russian_key():
    """Проверяет обработку русскоязычных ключей."""
    report = MedianCoffeeReport()
    data = [
        {"студент": "Мария", "coffee_spent": "150"},
        {"студент": "Мария", "coffee_spent": "250"},
    ]

    result = report.generate(data)

    assert len(result) == 1
    assert result[0]["student"] == "Мария"
    assert result[0]["median_coffee"] == 200.0


def test_median_coffee_generate_invalid_data():
    """Проверяет пропуск некорректных данных."""
    report = MedianCoffeeReport()
    data = [
        {"student": "Иван", "coffee_spent": "100"},  # валидно
        {"student": "Иван", "coffee_spent": "abc"},  # невалидно
        {"student": "Иван", "coffee_spent": "200"},  # валидно
        {"student": "Петр", "coffee_spent": None},  # невалидно
        {"student": "Петр"},  # нет поля coffee_spent
    ]

    result = report.generate(data)

    # Иван должен иметь [100, 200] -> медиана 150
    assert len(result) == 1
    assert result[0]["student"] == "Иван"
    assert result[0]["median_coffee"] == 150.0


def test_median_coffee_generate_empty_data():
    """Проверяет обработку пустых данных."""
    report = MedianCoffeeReport()
    result = report.generate([])
    assert result == []


def test_median_coffee_generate_missing_student():
    """Проверяет пропуск записей без студента."""
    report = MedianCoffeeReport()
    data = [
        {"coffee_spent": "100"},  # нет студента
        {"student": "Иван", "coffee_spent": "200"},
    ]

    result = report.generate(data)

    assert len(result) == 1
    assert result[0]["student"] == "Иван"
    assert result[0]["median_coffee"] == 200.0


def test_median_coffee_display(capsys):
    """Проверяет вывод отчета в консоль."""
    report = MedianCoffeeReport()
    test_data = [
        {"student": "Иван", "median_coffee": 500.0},
        {"student": "Петр", "median_coffee": 300.0},
    ]

    report.display(test_data)
    captured = capsys.readouterr()

    # Проверяем, что вывод содержит ожидаемые значения
    assert "Иван" in captured.out
    assert "Петр" in captured.out
    assert "500.00" in captured.out
    assert "300.00" in captured.out


def test_median_coffee_display_empty(capsys):
    """Проверяет вывод пустого отчета."""
    report = MedianCoffeeReport()

    report.display([])
    captured = capsys.readouterr()

    assert "Нет данных для отображения" in captured.out


def test_median_coffee_inherits_from_base():
    """Проверяет, что MedianCoffeeReport наследуется от BaseReport."""
    from gdp_analyzer.reports.base import BaseReport
    from gdp_analyzer.reports.median_coffee import MedianCoffeeReport

    assert issubclass(MedianCoffeeReport, BaseReport)

    report = MedianCoffeeReport()
    assert hasattr(report, "name")
    assert hasattr(report, "generate")
    assert hasattr(report, "display")
