from typing import Any
from .errors import MissingColumnError, UnknownColumnError

class Table:
    def __init__(self, columns: tuple[str, ...], records: list[dict[str, Any]] | None = None):
        self.columns = columns
        self.records: list[dict[str, Any]] = []
        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:
        missing = [col for col in self.columns if col not in record]
        if missing:
            raise MissingColumnError(f"Отсутствует поле '{missing[0]}' в записи.")
        extra = [col for col in record if col not in self.columns]
        if extra:
            raise UnknownColumnError(f"Поле '{extra[0]}' не определено в таблице.")
        self.records.append(record.copy())

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        unknown = [key for key in filters if key not in self.columns]
        if unknown:
            raise UnknownColumnError(f"Поле '{unknown[0]}' не определено в таблице.")
        if not filters:
            return [r.copy() for r in self.records]
        result = []
        for record in self.records:
            if all(record.get(key) == value for key, value in filters.items()):
                result.append(record.copy())
        return result

    def update_records(self, updates: dict[str, Any], **filters: Any) -> int:
        unknown = [key for key in updates if key not in self.columns]
        if unknown:
            raise UnknownColumnError(f"Поле '{unknown[0]}' не определено в таблице.")
        count = 0
        for record in self.records:
            if all(record.get(key) == value for key, value in filters.items()):
                for key, value in updates.items():
                    record[key] = value
                count += 1
        return count

    def delete_records(self, **filters: Any) -> int:
        if not filters:
            count = len(self.records)
            self.records.clear()
            return count
        new_records = []
        for record in self.records:
            if not all(record.get(key) == value for key, value in filters.items()):
                new_records.append(record)
        count = len(self.records) - len(new_records)
        self.records = new_records
        return count