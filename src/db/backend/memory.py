books = []
next_id = 1
def create_book(title, author, year, genre):
    global next_id
    if year < 0 or year > 2026:
            print("Ошибка: некорректный год!")
            return None
    if not title or not title.strip():
        print("Ошибка: название не может быть пустым!")
        return None
    if not author or not author.strip():
        print("Ошибка: автор не может быть пустым!")
        return None

    new_book = {
        "id": next_id,
        "title": title.strip(),
        "author": author.strip(),
        "year": year,
        "genre": genre.strip()
    }

    books.append(new_book)
    next_id = next_id + 1

    print("Книга добавлена! ID: {new_book['id']}")
    return new_book

def get_all_books():
    return books

def find_books(title=None, author=None, year=None, genre=None):
    result = []
    for book in books:
        if title is not None and book["title"] != title:
            continue
        if author is not None and book["author"] != author:
            continue
        if year is not None and book["year"] != year:
            continue
        if genre is not None and book["genre"] != genre:
            continue

        result.append(book)

    return result

def update_book(book_id, title=None, author=None, year=None, genre=None):
    for book in books:
        if book["id"] == book_id:
            if title is not None:
                book["title"] = title.strip()
            if author is not None:
                book["author"] = author.strip()
            if year is not None:
                if year < 0 or year > 2026:
                    print("Ошибка: некорректный год!")
                    return False
                book["year"] = year
            if genre is not None:
                book["genre"] = genre.strip()

            print(f"Книга с ID {book_id} обновлена!")
            return True

    print(f"Ошибка: книга с ID {book_id} не найдена!")
    return False


def delete_book(book_id):
    global books

    # Ищем индекс книги
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            print(f"Книга с ID {book_id} удалена!")
            return True

    print(f"Ошибка: книга с ID {book_id} не найдена!")
    return False

