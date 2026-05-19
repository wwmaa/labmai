import tempfile
import unittest
from src.db.backend.file import FileDatabase
from src.db.backend.errors import TableNotFoundError

class TestFileDatabase(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as d:
            db1 = FileDatabase(d)
            db1.create_table("books", ("id", "title", "author", "year", "genre"))
            db1.insert_record("books", {"id": 1, "title": "Война и мир", "author": "Толстой", "year": 1869, "genre": "Роман"})

            db2 = FileDatabase(d)
            records = db2.select_records("books")
            self.assertEqual(len(records), 1)
            self.assertEqual(records[0]["title"], "Война и мир")

    def test_select_with_filter(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("books", ("id", "title", "author", "year", "genre"))
            db.insert_record("books", {"id": 1, "title": "Война и мир", "author": "Толстой", "year": 1869, "genre": "Роман"})
            db.insert_record("books", {"id": 2, "title": "Анна Каренина", "author": "Толстой", "year": 1877, "genre": "Роман"})

            result = db.select_records("books", author="Толстой")
            self.assertEqual(len(result), 2)

            result = db.select_records("books", year=1869)
            self.assertEqual(len(result), 1)

    def test_update_record(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("books", ("id", "title", "author", "year", "genre"))
            db.insert_record("books", {"id": 1, "title": "Война и мир", "author": "Толстой", "year": 1869, "genre": "Роман"})

            db.update_records("books", {"year": 1870}, id=1)
            records = db.select_records("books")
            self.assertEqual(records[0]["year"], 1870)

    def test_delete_record(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            db.create_table("books", ("id", "title", "author", "year", "genre"))
            db.insert_record("books", {"id": 1, "title": "Война и мир", "author": "Толстой", "year": 1869, "genre": "Роман"})

            db.delete_records("books", id=1)
            records = db.select_records("books")
            self.assertEqual(len(records), 0)

    def test_missing_table(self):
        with tempfile.TemporaryDirectory() as d:
            db = FileDatabase(d)
            with self.assertRaises(TableNotFoundError):
                db.select_records("nonexistent")