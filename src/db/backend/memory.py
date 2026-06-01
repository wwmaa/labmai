from typing import Optional
from .errors import InvalidYearError, DuplicateIDError

type BookRecord = tuple[int, str, str, int, str]


class BookTable:
    def __init__(self) -> None:
        self._records: list[BookRecord] = []

    def create_record(
        self,
        book_id: int,
        title: str,
        author: str,
        year: int,
        genre: str,
    ) -> BookRecord:
        if year < 0:
            raise InvalidYearError("Поле year не может быть отрицательным.")

        if any(record[0] == book_id for record in self._records):
            raise DuplicateIDError(f"Запись с id={book_id} уже существует.")

        new_record: BookRecord = (
            book_id,
            title.strip(),
            author.strip(),
            year,
            genre.strip(),
        )
        self._records.append(new_record)
        return new_record

    def select_record(
        self,
        book_id: Optional[int] = None,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        genre: Optional[str] = None,
    ) -> list[BookRecord]:
        if all(param is None for param in [book_id, title, author, year, genre]):
            return self._records.copy()

        result: list[BookRecord] = []

        for record in self._records:
            if book_id is not None and record[0] != book_id:
                continue
            if title is not None and record[1] != title:
                continue
            if author is not None and record[2] != author:
                continue
            if year is not None and record[3] != year:
                continue
            if genre is not None and record[4] != genre:
                continue
            result.append(record)

        return result

    def update_record(
        self,
        book_id: int,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
        genre: Optional[str] = None,
    ) -> bool:
        for i, record in enumerate(self._records):
            if record[0] == book_id:
                new_record: BookRecord = (
                    record[0],
                    title.strip() if title else record[1],
                    author.strip() if author else record[2],
                    year if year is not None else record[3],
                    genre.strip() if genre else record[4],
                )
                self._records[i] = new_record
                return True
        return False

    def delete_record(self, book_id: int) -> bool:
        for i, record in enumerate(self._records):
            if record[0] == book_id:
                self._records.pop(i)
                return True
        return False

    def get_all_records(self) -> list[BookRecord]:
        return self._records.copy()

    def get_record_count(self) -> int:
        return len(self._records)

    def get_record_by_id(self, book_id: int) -> Optional[BookRecord]:
        """Возвращает запись по ID или None, если не найдена."""
        for record in self._records:
            if record[0] == book_id:
                return record
        return None