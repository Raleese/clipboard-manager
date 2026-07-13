import pyperclip
from database import Database

def start_clipboard_watcher(root, interval_ms=250):
    previous_text = pyperclip.paste()

    def watch_clipboard():
        nonlocal previous_text

        current_text = pyperclip.paste()
        if current_text != previous_text:
            previous_text = current_text
            save_text(current_text)

        root.after(interval_ms, watch_clipboard)

    def save_text(text):
        db = Database('clipboard_history.db')
        if db.get_count() >= 5:
            # Delete the oldest item
            db.delete_oldest_item()
        db.insert_item(text)

    root.after(interval_ms, watch_clipboard)