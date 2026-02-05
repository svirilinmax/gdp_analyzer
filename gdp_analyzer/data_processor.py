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

        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1251", "cp1252"]

        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    rows = list(reader)

                    if rows and any("country" in row for row in rows):
                        self._data.extend(rows)
                        return
            except UnicodeDecodeError:
                continue
            except Exception as e:
                if encoding == encodings[-1]:
                    raise ValueError(f"Ошибка чтения файла {file_path}: {e}")

        raise ValueError(
            f"Не удалось прочитать файл {file_path} с поддерживаемыми кодировками"
        )

    def get_data(self) -> List[Dict[str, Any]]:
        """Получение всех загруженных данных."""

        return self._data.copy()

    def clear_data(self) -> None:
        """Очистка загруженных данных."""

        self._data.clear()
