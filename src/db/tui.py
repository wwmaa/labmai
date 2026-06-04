from src.db.backend.memory import MemoryDatabase
from src.db.backend.file import FileDatabase
from src.db.backend.errors import (
    TableNotFoundError,
    TableAlreadyExistsError,
    MissingColumnError,
    UnknownColumnError,
    InvalidStorageDataError,
    DatabaseError
)


class TUI:
    def __init__(self):
        print("\nВыберите тип базы данных:")
        print("1. In-memory (данные не сохраняются)")
        print("2. File database (данные сохраняются в файлы)")
        choice = input("Ваш выбор (1 или 2): ").strip()
        if choice == "2":
            self.db = FileDatabase()
            print("Выбрана файловая база данных. Данные будут сохранены в папке 'data/'")
        else:
            self.db = MemoryDatabase()
            print("Выбрана in-memory база данных. Данные будут потеряны после закрытия программы.")

    def _get_schema(self, table_name: str):
        try:
            return self.db.get_table_schema(table_name)
        except TableNotFoundError as e:
            print(f"Ошибка: {e}")
            return None

    def run(self):
        while True:
            print("\n" + "=" * 40)
            print("      БАЗА ДАННЫХ КНИГ")
            print("=" * 40)
            print("1. Создать таблицу")
            print("2. Добавить книгу")
            print("3. Показать все книги")
            print("4. Найти книги")
            print("5. Обновить книгу")
            print("6. Удалить книгу")
            print("7. Показать все таблицы")
            print("0. Выход")
            print("=" * 40)

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                name = input("Имя таблицы: ").strip()
                cols = input("Колонки (через пробел): ").strip().split()
                try:
                    self.db.create_table(name, tuple(cols))
                    print(f"Таблица '{name}' создана!")
                except TableAlreadyExistsError as e:
                    print(f"Ошибка: {e}")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")

            elif choice == "2":
                name = input("Имя таблицы: ").strip()
                schema = self._get_schema(name)
                if schema is None:
                    continue
                try:
                    record = {}
                    for col in schema:
                        val = input(f"{col}: ").strip()
                        if col == "year":
                            val = int(val)
                        record[col] = val
                    self.db.insert_record(name, record)
                    print("Книга добавлена!")
                except (MissingColumnError, UnknownColumnError) as e:
                    print(f"Ошибка структуры: {e}")
                except ValueError:
                    print("Ошибка: год должен быть числом!")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")

            elif choice == "3":
                name = input("Имя таблицы: ").strip()
                try:
                    records = self.db.select_records(name)
                    if not records:
                        print("Нет записей.")
                    for r in records:
                        print(r)
                except TableNotFoundError as e:
                    print(f"Ошибка: {e}")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")

            elif choice == "4":
                name = input("Имя таблицы: ").strip()
                schema = self._get_schema(name)
                if schema is None:
                    continue
                try:
                    filters = {}
                    for col in schema:
                        val = input(f"{col} (Enter - пропустить): ").strip()
                        if val:
                            if col == "year":
                                val = int(val)
                            filters[col] = val
                    records = self.db.select_records(name, **filters)
                    if not records:
                        print("Не найдено.")
                    for r in records:
                        print(r)
                except UnknownColumnError as e:
                    print(f"Ошибка: поле '{e}' не найдено в таблице")
                except ValueError:
                    print("Ошибка: год должен быть числом!")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")

            elif choice == "5":
                name = input("Имя таблицы: ").strip()
                try:
                    book_id = int(input("ID книги: ").strip())
                except ValueError:
                    print("Ошибка: ID должен быть числом!")
                    continue
                schema = self._get_schema(name)
                if schema is None:
                    continue
                try:
                    updates = {}
                    for col in schema:
                        if col == "id":
                            continue
                        val = input(f"{col} (Enter - не менять): ").strip()
                        if val:
                            if col == "year":
                                val = int(val)
                            updates[col] = val
                    if not updates:
                        print("Нет данных для обновления.")
                        continue
                    count = self.db.update_records(name, updates, id=book_id)
                    if count > 0:
                        print("Книга обновлена!")
                    else:
                        print("Книга не найдена.")
                except (UnknownColumnError, MissingColumnError) as e:
                    print(f"Ошибка структуры: {e}")
                except ValueError:
                    print("Ошибка: год должен быть числом!")
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")

            elif choice == "6":
                name = input("Имя таблицы: ").strip()
                try:
                    book_id = int(input("ID книги: ").strip())
                except ValueError:
                    print("Ошибка: ID должен быть числом!")
                    continue
                confirm = input("Удалить? (да/нет): ").strip().lower()
                if confirm == "да":
                    try:
                        count = self.db.delete_records(name, id=book_id)
                        if count > 0:
                            print("Книга удалена!")
                        else:
                            print("Книга не найдена.")
                    except TableNotFoundError as e:
                        print(f"Ошибка: {e}")
                    except DatabaseError as e:
                        print(f"Ошибка базы данных: {e}")

            elif choice == "7":
                try:
                    tables = self.db.list_tables()
                    if not tables:
                        print("Нет таблиц.")
                    for t in tables:
                        print(t)
                except DatabaseError as e:
                    print(f"Ошибка базы данных: {e}")

            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор.")

            input("\nНажмите Enter для продолжения...")


def run():
    ui = TUI()
    ui.run()
