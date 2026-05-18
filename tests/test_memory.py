import unittest
from src.db.backend.memory import BookTable
from src.db.backend.errors import InvalidYearError, DuplicateIDError


class TestBookTable(unittest.TestCase):
    def setUp(self):
        self.table = BookTable()
        self.test_records = [
            (1, "Война и мир", "Лев Толстой", 1869, "Роман"),
            (2, "Преступление и наказание", "Фёдор Достоевский", 1866, "Роман"),
            (3, "Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман"),
            (4, "Евгений Онегин", "Александр Пушкин", 1833, "Поэма"),
            (5, "Мёртвые души", "Николай Гоголь", 1842, "Поэма"),
        ]

    def test_create_record_success(self):
        record = self.table.create_record(1, "Война и мир", "Лев Толстой", 1869, "Роман")
        self.assertEqual(record, (1, "Война и мир", "Лев Толстой", 1869, "Роман"))
        self.assertEqual(self.table.get_record_count(), 1)

    def test_create_record_multiple(self):
        for record in self.test_records:
            created = self.table.create_record(*record)
            self.assertEqual(created, record)
        self.assertEqual(self.table.get_record_count(), 5)

    def test_create_record_negative_year(self):
        with self.assertRaises(InvalidYearError):
            self.table.create_record(1, "Книга", "Автор", -5, "Жанр")

    def test_create_record_duplicate_id(self):
        self.table.create_record(1, "Война и мир", "Лев Толстой", 1869, "Роман")
        with self.assertRaises(DuplicateIDError):
            self.table.create_record(1, "Другая книга", "Другой автор", 2000, "Жанр")

    def test_select_all(self):
        for record in self.test_records:
            self.table.create_record(*record)
        all_records = self.table.select_record()
        self.assertEqual(len(all_records), 5)
        self.assertEqual(all_records, self.test_records)

    def test_select_by_id(self):
        for record in self.test_records:
            self.table.create_record(*record)
        result = self.table.select_record(book_id=2)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (2, "Преступление и наказание", "Фёдор Достоевский", 1866, "Роман"))

    def test_select_by_author(self):
        for record in self.test_records:
            self.table.create_record(*record)
        result = self.table.select_record(author="Михаил Булгаков")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (3, "Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман"))

    def test_select_by_year(self):
        for record in self.test_records:
            self.table.create_record(*record)
        result = self.table.select_record(year=1869)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], (1, "Война и мир", "Лев Толстой", 1869, "Роман"))

    def test_select_by_genre(self):
        for record in self.test_records:
            self.table.create_record(*record)
        result = self.table.select_record(genre="Поэма")
        self.assertEqual(len(result), 2)

    def test_select_empty_table(self):
        result = self.table.select_record()
        self.assertEqual(result, [])

    def test_select_no_matches(self):
        for record in self.test_records:
            self.table.create_record(*record)
        result = self.table.select_record(author="Несуществующий автор")
        self.assertEqual(result, [])

    def test_update_record_success(self):
        self.table.create_record(1, "Война и мир", "Лев Толстой", 1869, "Роман")
        result = self.table.update_record(1, title="Война и мир (том 1)", year=1867)
        self.assertTrue(result)
        updated = self.table.select_record(book_id=1)
        self.assertEqual(updated[0][1], "Война и мир (том 1)")
        self.assertEqual(updated[0][3], 1867)

    def test_update_record_not_found(self):
        result = self.table.update_record(999, title="Нет такой книги")
        self.assertFalse(result)

    def test_update_record_partial(self):
        self.table.create_record(1, "Война и мир", "Лев Толстой", 1869, "Роман")
        self.table.update_record(1, year=1870)
        updated = self.table.select_record(book_id=1)[0]
        self.assertEqual(updated[1], "Война и мир")
        self.assertEqual(updated[3], 1870)

    def test_delete_record_success(self):
        self.table.create_record(1, "Война и мир", "Лев Толстой", 1869, "Роман")
        self.table.create_record(2, "Преступление и наказание", "Фёдор Достоевский", 1866, "Роман")
        result = self.table.delete_record(1)
        self.assertTrue(result)
        self.assertEqual(self.table.get_record_count(), 1)
        all_records = self.table.select_record()
        self.assertEqual(all_records[0][0], 2)

    def test_delete_record_not_found(self):
        result = self.table.delete_record(999)
        self.assertFalse(result)

    def test_delete_record_empty_table(self):
        result = self.table.delete_record(1)
        self.assertFalse(result)

    def test_get_all_records(self):
        for record in self.test_records:
            self.table.create_record(*record)
        all_records = self.table.get_all_records()
        self.assertEqual(len(all_records), 5)
        self.assertEqual(all_records, self.test_records)

    def test_get_record_count(self):
        self.assertEqual(self.table.get_record_count(), 0)
        self.table.create_record(1, "Война и мир", "Лев Толстой", 1869, "Роман")
        self.assertEqual(self.table.get_record_count(), 1)
        self.table.create_record(2, "Преступление и наказание", "Фёдор Достоевский", 1866, "Роман")
        self.assertEqual(self.table.get_record_count(), 2)


if __name__ == "__main__":
    unittest.main()