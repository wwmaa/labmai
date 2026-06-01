from src.db.backend.memory import BookTable


class TUI:
    def __init__(self):
        self.db = BookTable()
        print("\nДобро пожаловать в базу данных книг!")

    def run(self):
        while True:
            print("\n" + "=" * 40)
            print("      БАЗА ДАННЫХ КНИГ")
            print("=" * 40)
            print("1. Добавить книгу")
            print("2. Показать все книги")
            print("3. Найти книги")
            print("4. Обновить книгу")
            print("5. Удалить книгу")
            print("6. Показать все таблицы")
            print("0. Выход")
            print("=" * 40)

            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._add_book()

            elif choice == "2":
                self._show_all_books()

            elif choice == "3":
                self._find_books()

            elif choice == "4":
                self._update_book()

            elif choice == "5":
                self._delete_book()

            elif choice == "6":
                self._show_tables()

            elif choice == "0":
                print("До свидания!")
                break

            else:
                print("Неверный выбор. Попробуйте снова.")

            input("\nНажмите Enter для продолжения...")

    def _add_book(self):
        print("\n--- ДОБАВЛЕНИЕ КНИГИ ---")
        try:
            book_id = int(input("ID: ").strip())
            title = input("Название: ").strip()
            author = input("Автор: ").strip()
            year = int(input("Год издания: ").strip())
            genre = input("Жанр: ").strip()

            record = self.db.create_record(book_id, title, author, year, genre)
            print(f"Книга добавлена! ID: {record[0]}")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _show_all_books(self):
        print("\n--- ВСЕ КНИГИ ---")
        records = self.db.get_all_records()
        if not records:
            print("Нет книг в базе данных.")
            return
        print("\nID | Название | Автор | Год | Жанр")
        print("-" * 60)
        for r in records:
            print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
        print(f"\nВсего книг: {len(records)}")

    def _find_books(self):
        print("\n--- ПОИСК КНИГ ---")
        print("(оставьте поле пустым, чтобы не учитывать его)")
        try:
            book_id = input("ID: ").strip()
            book_id = int(book_id) if book_id else None

            title = input("Название: ").strip()
            title = title if title else None

            author = input("Автор: ").strip()
            author = author if author else None

            year = input("Год: ").strip()
            year = int(year) if year else None

            genre = input("Жанр: ").strip()
            genre = genre if genre else None

            records = self.db.select_record(
                book_id=book_id,
                title=title,
                author=author,
                year=year,
                genre=genre
            )

            if not records:
                print("\nКниги не найдены.")
                return

            print(f"\nНайдено книг: {len(records)}")
            print("\nID | Название | Автор | Год | Жанр")
            print("-" * 60)
            for r in records:
                print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _update_book(self):
        print("\n--- ОБНОВЛЕНИЕ КНИГИ ---")
        try:
            book_id = int(input("Введите ID книги для обновления: ").strip())

            book = self.db.get_record_by_id(book_id)
            if not book:
                print(f"Книга с ID {book_id} не найдена.")
                return

            print(f"\nТекущие данные: {book[1]} | {book[2]} | {book[3]} | {book[4]}")
            print("\n(оставьте поле пустым, чтобы не менять)")

            title = input(f"Новое название [{book[1]}]: ").strip()
            title = title if title else None

            author = input(f"Новый автор [{book[2]}]: ").strip()
            author = author if author else None

            year = input(f"Новый год [{book[3]}]: ").strip()
            year = int(year) if year else None

            genre = input(f"Новый жанр [{book[4]}]: ").strip()
            genre = genre if genre else None

            result = self.db.update_record(book_id, title, author, year, genre)
            if result:
                print("Книга успешно обновлена!")
            else:
                print("Ошибка при обновлении.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _delete_book(self):
        print("\n--- УДАЛЕНИЕ КНИГИ ---")
        try:
            book_id = int(input("Введите ID книги для удаления: ").strip())

            book = self.db.get_record_by_id(book_id)
            if not book:
                print(f"Книга с ID {book_id} не найдена.")
                return

            print(f"\nКнига для удаления: {book[1]} | {book[2]}")
            confirm = input("Вы уверены? (да/нет): ").strip().lower()

            if confirm == "да":
                result = self.db.delete_record(book_id)
                if result:
                    print("Книга успешно удалена!")
                else:
                    print("Ошибка при удалении.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def _show_tables(self):
        print("\n--- ТАБЛИЦЫ ---")
        print("books (таблица книг)")


def run():
    ui = TUI()
    ui.run()