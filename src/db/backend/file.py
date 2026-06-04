import json
from pathlib import Path
from .database import Database
from .errors import InvalidStorageDataError, TableNotFoundError
from .table import Table

class FileDatabase(Database):
    def __init__(self, directory: str = "data"):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)

    def _get_table_path(self, table_name: str) -> Path:
        return self.directory / f"{table_name}.json"

    def _table_exists(self, table_name: str) -> bool:
        return self._get_table_path(table_name).exists()

    def _load_table(self, table_name: str) -> Table:
        path = self._get_table_path(table_name)
        if not path.exists():
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise InvalidStorageDataError("Файл таблицы содержит некорректный JSON.") from e
        except PermissionError as e:
            raise InvalidStorageDataError(f"Нет доступа к файлу: {path}") from e
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка при чтении файла: {e}") from e
        if not isinstance(data, dict):
            raise InvalidStorageDataError("Файл таблицы должен содержать JSON-объект (словарь).")
        if "columns" not in data or "records" not in data:
            raise InvalidStorageDataError("Файл таблицы имеет некорректную структуру.")
        if not isinstance(data["columns"], list):
            raise InvalidStorageDataError("Поле 'columns' должно быть списком.")
        if not isinstance(data["records"], list):
            raise InvalidStorageDataError("Поле 'records' должно быть списком.")
        for col in data["columns"]:
            if not isinstance(col, str):
                raise InvalidStorageDataError("Имена колонок должны быть строками.")
        for record in data["records"]:
            if not isinstance(record, dict):
                raise InvalidStorageDataError("Записи должны быть словарями.")
        return Table(tuple(data["columns"]), data["records"])

    def _save_table(self, table_name: str, table: Table) -> None:
        path = self._get_table_path(table_name)
        data = {
            "columns": list(table.columns),
            "records": table.records
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except PermissionError as e:
            raise InvalidStorageDataError(f"Нет доступа для записи в файл: {path}") from e
        except OSError as e:
            raise InvalidStorageDataError(f"Ошибка при записи файла: {e}") from e

    def list_tables(self) -> list[str]:
        tables = []
        for file in self.directory.glob("*.json"):
            tables.append(file.stem)
        return tables