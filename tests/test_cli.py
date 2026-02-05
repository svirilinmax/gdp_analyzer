import csv
import sys
import tempfile
from io import StringIO
from unittest.mock import patch

import pytest

from gdp_analyzer.cli import main, parse_args


def test_parse_args():
    """Тест парсинга аргументов."""

    test_args = ["--files", "economic1.csv", "economic2.csv", "--report", "average-gdp"]

    with patch.object(sys, "argv", ["script.py"] + test_args):
        args = parse_args()

        assert args.files == ["economic1.csv", "economic2.csv"]
        assert args.report == "average-gdp"


def test_parse_args_missing_files(capsys):
    """Тест парсинга аргументов при отсутствии файлов"""

    test_args = ["--report", "average-gdp"]

    with patch.object(sys, "argv", ["script.py"] + test_args):
        with pytest.raises(SystemExit) as excinfo:
            main()

    assert excinfo.value.code == 1

    captured = capsys.readouterr()

    assert "Ошибка: требуются оба аргумента --files и --report" in captured.err


def test_main_success():
    """Тест успешного выполнения main."""

    temp_files = []

    for i in range(2):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=["country", "year", "gdp"])
            writer.writeheader()
            writer.writerow(
                {"country": f"Country{i}", "year": "2023", "gdp": str(1000 + i)}
            )
            temp_files.append(f.name)

    try:
        test_args = ["--files", temp_files[0], temp_files[1], "--report", "average-gdp"]

        with patch.object(sys, "argv", ["script.py"] + test_args):
            with patch("sys.stdout", new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                # Проверяем, что вывод содержит ожидаемые данные
                assert "Country" in output or "country" in output
                assert "gdp" in output
    finally:
        import os

        for file in temp_files:
            if os.path.exists(file):
                os.unlink(file)


def test_main_file_not_found(capsys):
    """Тест обработки отсутствующего файла в функции main"""

    test_args = ["--files", "non_existent.csv", "--report", "average-gdp"]

    with patch.object(sys, "argv", ["script.py"] + test_args):
        with pytest.raises(SystemExit):
            main()

        captured = capsys.readouterr()

        output = captured.out + captured.err
        assert "Файл не найден" in output or "не найден" in output.lower()


def test_main_invalid_report(tmp_path, capsys):
    """Тест обработки неверного (несуществующего) отчета в функции main"""

    temp_file = tmp_path / "test_data.csv"
    temp_file.write_text("country,year,gdp\nUSA,2023,1000")

    test_args = ["--files", str(temp_file), "--report", "invalid-report"]

    with patch.object(sys, "argv", ["script.py"] + test_args):
        with pytest.raises(SystemExit) as exc_info:
            main()

        captured = capsys.readouterr()

    assert exc_info.value.code == 1
    assert "не найден" in (captured.out + captured.err)


def test_list_reports(capsys):
    """Тест флага --list-reports."""

    test_args = ["--list-reports"]

    with patch.object(sys, "argv", ["script.py"] + test_args):
        main()
        captured = capsys.readouterr()

        assert "Доступные отчеты" in captured.out
        assert "average-gdp" in captured.out
