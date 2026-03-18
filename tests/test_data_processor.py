import csv
import tempfile

import pytest

from gdp_analyzer.data_processor import DataProcessor


def test_data_processor_initialization():
    """Тест инициализации DataProcessor."""

    processor = DataProcessor()
    assert processor.get_data() == []


def test_load_csv():
    """Тест загрузки CSV файла."""

    processor = DataProcessor()

    # Создаем временный CSV файл
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=["country", "year", "gdp"])
        writer.writeheader()
        writer.writerow({"country": "USA", "year": "2023", "gdp": "1000"})
        writer.writerow({"country": "China", "year": "2023", "gdp": "800"})
        temp_file = f.name

    try:
        processor.load_csv(temp_file)
        data = processor.get_data()
        assert len(data) == 2
        assert data[0]["country"] == "USA"
        assert data[1]["country"] == "China"
    finally:
        import os

        os.unlink(temp_file)


def test_load_csv_file_not_found():
    """Тест загрузки несуществующего файла."""

    processor = DataProcessor()

    with pytest.raises(FileNotFoundError):
        processor.load_csv("non_existent_file.csv")


def test_load_csv_invalid_encoding(tmp_path):
    """Тест загрузки файла с неподдерживаемой кодировкой."""
    processor = DataProcessor()
    temp_file = tmp_path / "wrong_encoding.csv"
    temp_file.write_bytes(b"\xff\xfe\xfd\x12\x34")

    with pytest.raises(ValueError, match="Не удалось подобрать кодировку для файла"):
        processor.load_csv(str(temp_file))


def test_clear_data():
    """Тест очистки данных."""

    processor = DataProcessor()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        writer = csv.DictWriter(f, fieldnames=["country", "year", "gdp"])
        writer.writeheader()
        writer.writerow({"country": "USA", "year": "2023", "gdp": "1000"})
        temp_file = f.name

    try:
        processor.load_csv(temp_file)
        assert len(processor.get_data()) == 1
        processor.clear_data()
        assert len(processor.get_data()) == 0
    finally:
        import os

        os.unlink(temp_file)
