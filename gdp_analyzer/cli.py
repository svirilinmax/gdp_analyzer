import argparse
import sys

from .data_processor import DataProcessor
from .exceptions import ReportNotFoundError
from .reports.registry import ReportRegistry


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""

    parser = argparse.ArgumentParser(
        description="Анализ макроэкономических данных по странам",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s --files data1.csv data2.csv --report average-gdp
  %(prog)s --list-reports
        """,
    )

    parser.add_argument("--files", nargs="+", help="Пути к CSV файлам с данными")

    parser.add_argument(
        "--report", help="Название отчета для генерации (например, average-gdp)"
    )

    parser.add_argument(
        "--list-reports",
        action="store_true",
        help="Показать список доступных отчетов и выйти",
    )

    return parser.parse_args()


def main() -> None:
    """Основная функция приложения."""

    try:
        args = parse_args()

        # Обработка флага --list-reports
        if args.list_reports:
            reports = ReportRegistry.list_reports()
            if reports:
                print("Доступные отчеты:")
                for report_name in reports:
                    print(f"  • {report_name}")
            else:
                print("Нет зарегистрированных отчетов")
            return

        # Проверка обязательных аргументов
        if not args.files or not args.report:
            print("Ошибка: требуются оба аргумента --files и --report", file=sys.stderr)
            print(
                "Используйте --list-reports для просмотра доступных отчетов",
                file=sys.stderr,
            )
            print("Или --help для справки")
            sys.exit(1)

        processor = DataProcessor()
        for file_path in args.files:
            processor.load_csv(file_path)

        report_generator = ReportRegistry.get_report(args.report)

        if report_generator is None:
            raise ReportNotFoundError(
                f"Отчет '{args.report}' не найден. "
                f"Доступные отчеты: {', '.join(ReportRegistry.list_reports())}"
            )

        report_data = report_generator.generate(processor.get_data())
        report_generator.display(report_data)

    except (ReportNotFoundError, FileNotFoundError) as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
