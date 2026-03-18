import csv
import os
from typing import Any, Dict, List


class DataProcessor:
    """Класс для загрузки и обработки CSV данных."""

    def __init__(self) -> None:
        self._data: List[Dict[str, Any]] = []

    def load_csv(self, file_path: str) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        # Оставляем только самые вероятные кодировки
        encodings = ["utf-8", "utf-8-sig", "cp1251", "cp866"]

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)

                    if not reader.fieldnames or len(rows) == 0:
                        continue

                    self._data.extend(rows)
                    return

            except (UnicodeDecodeError, UnicodeError):
                continue
            except Exception as e:
                raise ValueError(f"Критическая ошибка при чтении {file_path}: {e}")

        raise ValueError(f"Не удалось подобрать кодировку для файла {file_path}")

    def get_data(self) -> List[Dict[str, Any]]:
        """Получение всех загруженных данных."""

        return self._data.copy()

    def clear_data(self) -> None:
        """Очистка загруженных данных."""

        self._data.clear()
