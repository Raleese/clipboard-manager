import pyperclip
from database import Database

def start_clipboard_watcher(root, interval_ms=250, db=None, item_limit=5):
    previous_text = pyperclip.paste()

    def watch_clipboard():
        nonlocal previous_text

        current_text = pyperclip.paste()
        if current_text != previous_text:
            previous_text = current_text
            save_text(current_text)

        root.after(interval_ms, watch_clipboard)

    def save_text(text):
        if db.get_count() >= item_limit:
            # Delete the oldest item
            db.delete_oldest_item()
        db.insert_item(text)

    root.after(interval_ms, watch_clipboard)
