from .backend import memory
def show_menu():
    print("\n" + "=" * 40)
    print("База данных книг")
    print("=" * 40)
    print("1. Добавить книгу")
    print("2. Показать все книги")
    print("3. Найти книги")
    print("4. Обновить книгу")
    print("5. Удалить книгу")
    print("0. Выход")
    print("=" * 40)

def add_book_ui():

    print("\nДобавление книги")
    title = input("Название: ").strip()
    if not title:
        print("Ошибка: название не может быть пустым!")
        return

    author = input("Автор: ").strip()
    if not author:
        print("Ошибка: автор не может быть пустым!")
        return

    try:
        year = int(input("Год издания: "))
    except ValueError:
        print("Ошибка: введите число!")
        return

    genre = input("Жанр: ").strip()

    memory.create_book(title, author, year, genre)


def show_all_books_ui():
    print("\n--- ВСЕ КНИГИ ---")

    books = memory.get_all_books()

    if not books:
        print("Нет книг в базе данных.")
        return

    print("\nID | Название | Автор | Год | Жанр")
    print("-" * 60)

    for book in books:
        print(f"{book['id']} | {book['title']} | {book['author']} | {book['year']} | {book['genre']}")

    print(f"\nВсего книг: {len(books)}")


def find_books_ui():
    print("\n--- ПОИСК КНИГ ---")
    print("(оставьте поле пустым, чтобы не учитывать его)")

    title = input("Название: ").strip()
    if title == "":
        title = None

    author = input("Автор: ").strip()
    if author == "":
        author = None

    year_input = input("Год: ").strip()
    if year_input == "":
        year = None
    else:
        try:
            year = int(year_input)
        except ValueError:
            print("Ошибка: год должен быть числом!")
            return

    genre = input("Жанр: ").strip()
    if genre == "":
        genre = None

    found = memory.find_books(title, author, year, genre)
    if not found:
        print("Книги не найдены.")
        return
    print(f"\nНайдено книг: {len(found)}")
    print("\nID | Название | Автор | Год | Жанр")
    print("-" * 60)
    for book in found:
        print(f"{book['id']} | {book['title']} | {book['author']} | {book['year']} | {book['genre']}")

def update_book_ui():
    print("\nОбновление инфформации о книге")

    try:
        book_id = int(input("Введите ID книги для обновления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return

    books = memory.get_all_books()
    book_to_update = None

    for book in books:
        if book["id"] == book_id:
            book_to_update = book
            break

    if not book_to_update:
        print(f"Книга с ID {book_id} не найдена!")
        return

    print(
        f"\nТекущие данные: {book_to_update['title']} | {book_to_update['author']} | {book_to_update['year']} | {book_to_update['genre']}")
    print("\n(оставьте поле пустым, чтобы не менять)")

    title = input(f"Новое название [{book_to_update['title']}]: ").strip()
    if title == "":
        title = None

    author = input(f"Новый автор [{book_to_update['author']}]: ").strip()
    if author == "":
        author = None

    year_input = input(f"Новый год [{book_to_update['year']}]: ").strip()
    if year_input == "":
        year = None
    else:
        try:
            year = int(year_input)
        except ValueError:
            print("Ошибка: год должен быть числом!")
            return

    genre = input(f"Новый жанр [{book_to_update['genre']}]: ").strip()
    if genre == "":
        genre = None

    memory.update_book(book_id, title, author, year, genre)


def delete_book_ui():
    print("\nУдаление книги")

    try:
        book_id = int(input("Введите ID книги для удаления: "))
    except ValueError:
        print("Ошибка: ID должен быть числом!")
        return
    books = memory.get_all_books()
    book_exists = False

    for book in books:
        if book["id"] == book_id:
            book_exists = True
            print(f"\nКнига для удаления: {book['title']} | {book['author']}")
            break

    if not book_exists:
        print(f"Книга с ID {book_id} не найдена!")
        return
    confirm = input("\nВы уверены, что хотите удалить? (да/нет): ").strip().lower()

    if confirm == "да":
        memory.delete_book(book_id)
    else:
        print("Удаление отменено.")


def run():
    print("\nДобро пожаловать в базу данных книг!")

    while True:
        show_menu()

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            add_book_ui()
        elif choice == "2":
            show_all_books_ui()
        elif choice == "3":
            find_books_ui()
        elif choice == "4":
            update_book_ui()
        elif choice == "5":
            delete_book_ui()
        elif choice == "0":
            print("\nДо свидания!")
            break
        else:
            print("Ошибка: неверный выбор. Попробуйте снова.")

        input("\nНажмите Enter для продолжения")