import unittest
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import TableAlreadyExistsError, TableNotFoundError, MissingColumnError, UnknownColumnError


class TestMemoryDatabase(unittest.TestCase):
    def setUp(self):
        self.db = MemoryDatabase()

    def test_create_table(self):
        self.db.create_table("books", ("id", "title", "author", "year", "genre"))
        self.assertTrue(self.db._table_exists("books"))

    def test_create_table_already_exists(self):
        self.db.create_table("books", ("id", "title"))
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table("books", ("id", "title"))

    def test_insert_record(self):
        self.db.create_table("books", ("id", "title", "author"))
        self.db.insert_record("books", {"id": 1, "title": "Война и мир", "author": "Толстой"})
        records = self.db.select_records("books")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["title"], "Война и мир")

    def test_insert_record_missing_column(self):
        self.db.create_table("books", ("id", "title", "author"))
        with self.assertRaises(MissingColumnError):
            self.db.insert_record("books", {"id": 1, "title": "Война и мир"})

    def test_insert_record_unknown_column(self):
        self.db.create_table("books", ("id", "title"))
        with self.assertRaises(UnknownColumnError):
            self.db.insert_record("books", {"id": 1, "title": "Война и мир", "extra": "лишнее"})

    def test_select_records_no_filters(self):
        self.db.create_table("books", ("id", "title"))
        self.db.insert_record("books", {"id": 1, "title": "Война и мир"})
        self.db.insert_record("books", {"id": 2, "title": "Анна Каренина"})
        records = self.db.select_records("books")
        self.assertEqual(len(records), 2)

    def test_select_records_with_filter(self):
        self.db.create_table("books", ("id", "title"))
        self.db.insert_record("books", {"id": 1, "title": "Война и мир"})
        self.db.insert_record("books", {"id": 2, "title": "Анна Каренина"})
        records = self.db.select_records("books", title="Война и мир")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], 1)

    def test_select_records_table_not_found(self):
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("nonexistent")

    def test_update_records(self):
        self.db.create_table("books", ("id", "title", "year"))
        self.db.insert_record("books", {"id": 1, "title": "Война и мир", "year": 1869})
        count = self.db.update_records("books", {"year": 1870}, id=1)
        self.assertEqual(count, 1)
        records = self.db.select_records("books", id=1)
        self.assertEqual(records[0]["year"], 1870)

    def test_update_records_not_found(self):
        self.db.create_table("books", ("id", "title"))
        count = self.db.update_records("books", {"title": "Новое"}, id=999)
        self.assertEqual(count, 0)

    def test_delete_records(self):
        self.db.create_table("books", ("id", "title"))
        self.db.insert_record("books", {"id": 1, "title": "Война и мир"})
        self.db.insert_record("books", {"id": 2, "title": "Анна Каренина"})
        count = self.db.delete_records("books", id=1)
        self.assertEqual(count, 1)
        records = self.db.select_records("books")
        self.assertEqual(len(records), 1)

    def test_delete_records_all(self):
        self.db.create_table("books", ("id", "title"))
        self.db.insert_record("books", {"id": 1, "title": "Война и мир"})
        count = self.db.delete_records("books")
        self.assertEqual(count, 1)
        records = self.db.select_records("books")
        self.assertEqual(len(records), 0)

    def test_list_tables(self):
        self.db.create_table("books", ("id", "title"))
        self.db.create_table("authors", ("id", "name"))
        tables = self.db.list_tables()
        self.assertEqual(len(tables), 2)
        self.assertIn("books", tables)
        self.assertIn("authors", tables)

    def test_get_table_schema(self):
        self.db.create_table("books", ("id", "title", "author"))
        schema = self.db.get_table_schema("books")
        self.assertEqual(schema, ("id", "title", "author"))
