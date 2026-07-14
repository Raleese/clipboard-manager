import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import Database


class DatabaseTests(unittest.TestCase):
    def test_insert_fetch_and_count_items(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "clipboard_history.db")
            database = Database(database_path)
            try:
                database.insert_item("first")
                database.insert_item("second")

                self.assertEqual(database.get_count(), 2)
                self.assertEqual(
                    database.fetch_all_items(),
                    [(2, "second"), (1, "first")],
                )
            finally:
                database.close()

    def test_delete_oldest_item_removes_lowest_id(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            database_path = os.path.join(temp_dir, "clipboard_history.db")
            database = Database(database_path)
            try:
                database.insert_item("first")
                database.insert_item("second")
                database.delete_oldest_item()

                self.assertEqual(database.get_count(), 1)
                self.assertEqual(database.fetch_all_items(), [(2, "second")])
            finally:
                database.close()


if __name__ == "__main__":
    unittest.main()