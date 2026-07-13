import tkinter as tk
from hotkeys import register_hold
from clipboard import start_clipboard_watcher
from database import Database
import os
from pathlib import Path

local_app_data = os.environ.get("LOCALAPPDATA")
if local_app_data:
    app_data_folder = Path(local_app_data) / "ClipboardManager"
else:
    app_data_folder = Path.home() / "AppData" / "Local" / "ClipboardManager"
app_data_folder.mkdir(parents=True, exist_ok=True)

db = Database(app_data_folder / "clipboard_history.db")

root = tk.Tk()
root.title("Clipboard Manager")
root.withdraw()  # Hide the main window

clipboard_list = tk.Listbox(root, width=60, height=10)
clipboard_list.pack(padx=15, pady=15)


def hide_manager():
    root.withdraw()

def refresh_clipboard_list():
    clipboard_list.delete(0, tk.END)

    for item_id, content in db.fetch_all_items():
        clipboard_list.insert(tk.END, content)


def show_manager():
    refresh_clipboard_list()
    root.update_idletasks()

    window_width = root.winfo_reqwidth()
    window_height = root.winfo_reqheight()
    cursor_x = root.winfo_pointerx()
    cursor_y = root.winfo_pointery()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = min(max(cursor_x - window_width // 2, 0), screen_width - window_width)
    y_position = min(max(cursor_y - window_height // 2, 0), screen_height - window_height)

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    root.deiconify()
    root.lift()
    root.focus_force()


def open_manager():
    # The keyboard listener is on a separate thread.
    root.after(0, show_manager)


root.protocol("WM_DELETE_WINDOW", hide_manager)


register_hold(open_manager, 0.5)
start_clipboard_watcher(root, db=db, item_limit=5)
root.mainloop()
