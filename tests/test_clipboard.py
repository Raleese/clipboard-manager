import os
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from clipboard import start_clipboard_watcher


class FakeRoot:
    def __init__(self):
        self.scheduled_callbacks = []

    def after(self, interval_ms, callback):
        self.scheduled_callbacks.append((interval_ms, callback))


class FakeDatabase:
    def __init__(self, count=0):
        self.count = count
        self.saved_items = []
        self.deleted_oldest_item_called = 0

    def get_count(self):
        return self.count

    def delete_oldest_item(self):
        self.deleted_oldest_item_called += 1
        if self.count > 0:
            self.count -= 1

    def insert_item(self, content):
        self.saved_items.append(content)
        self.count += 1


class ClipboardWatcherTests(unittest.TestCase):
    def test_watcher_saves_only_changed_text(self):
        fake_root = FakeRoot()
        fake_database = FakeDatabase()

        with patch("clipboard.pyperclip.paste", side_effect=["first", "first", "second", "second"]):
            start_clipboard_watcher(fake_root, interval_ms=250, db=fake_database, item_limit=5)

            self.assertEqual(len(fake_root.scheduled_callbacks), 1)

            _, first_callback = fake_root.scheduled_callbacks.pop(0)
            first_callback()
            _, second_callback = fake_root.scheduled_callbacks.pop(0)
            second_callback()
            _, third_callback = fake_root.scheduled_callbacks.pop(0)
            third_callback()

        self.assertEqual(fake_database.saved_items, ["second"])

    def test_watcher_deletes_oldest_item_at_capacity(self):
        fake_root = FakeRoot()
        fake_database = FakeDatabase(count=5)

        with patch("clipboard.pyperclip.paste", side_effect=["initial", "updated"]):
            start_clipboard_watcher(fake_root, interval_ms=250, db=fake_database, item_limit=5)
            _, callback = fake_root.scheduled_callbacks.pop(0)
            callback()

        self.assertEqual(fake_database.deleted_oldest_item_called, 1)
        self.assertEqual(fake_database.saved_items, ["updated"])
        self.assertEqual(fake_database.count, 5)


if __name__ == "__main__":
    unittest.main()