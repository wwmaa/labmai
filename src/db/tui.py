from src.db.backend.memory import MemoryDatabase
from src.db.backend.file import FileDatabase

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
                except Exception as e:
                    print(f"Ошибка: {e}")

            elif choice == "2":
                name = input("Имя таблицы: ").strip()
                try:
                    table = self.db._load_table(name)
                    record = {}
                    for col in table.columns:
                        val = input(f"{col}: ").strip()
                        if col == "year":
                            val = int(val)
                        record[col] = val
                    self.db.insert_record(name, record)
                    print("Книга добавлена!")
                except Exception as e:
                    print(f"Ошибка: {e}")

            elif choice == "3":
                name = input("Имя таблицы: ").strip()
                try:
                    records = self.db.select_records(name)
                    if not records:
                        print("Нет записей.")
                    for r in records:
                        print(r)
                except Exception as e:
                    print(f"Ошибка: {e}")

            elif choice == "4":
                name = input("Имя таблицы: ").strip()
                try:
                    table = self.db._load_table(name)
                    filters = {}
                    for col in table.columns:
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
                except Exception as e:
                    print(f"Ошибка: {e}")

            elif choice == "5":
                name = input("Имя таблицы: ").strip()
                try:
                    table = self.db._load_table(name)
                    book_id = int(input("ID книги: ").strip())
                    updates = {}
                    for col in table.columns:
                        if col == "id":
                            continue
                        val = input(f"{col} (Enter - не менять): ").strip()
                        if val:
                            if col == "year":
                                val = int(val)
                            updates[col] = val
                    count = self.db.update_records(name, updates, id=book_id)
                    if count > 0:
                        print("Книга обновлена!")
                    else:
                        print("Книга не найдена.")
                except Exception as e:
                    print(f"Ошибка: {e}")

            elif choice == "6":
                name = input("Имя таблицы: ").strip()
                book_id = int(input("ID книги: ").strip())
                confirm = input("Удалить? (да/нет): ").strip().lower()
                if confirm == "да":
                    count = self.db.delete_records(name, id=book_id)
                    if count > 0:
                        print("Книга удалена!")
                    else:
                        print("Книга не найдена.")

            elif choice == "7":
                try:
                    import os
                    if os.path.exists("data"):
                        files = os.listdir("data")
                        for f in files:
                            print(f.replace(".json", ""))
                    else:
                        print("Нет таблиц.")
                except:
                    print("Нет таблиц.")

            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор.")

            input("\nНажмите Enter для продолжения...")


def run():
    ui = TUI()
    ui.run()