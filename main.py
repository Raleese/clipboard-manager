import tkinter as tk
from hotkeys import register_hold
from clipboard import start_clipboard_watcher
from database import Database

db = Database('clipboard_history.db')  # Initialize the database

root = tk.Tk()
root.title("Clipboard Manager")
root.withdraw()  # Hide the main window

clipboard_list = tk.Listbox(root, width=60, height=10)
clipboard_list.pack(padx=15, pady=15)

def refresh_clipboard_list():
    clipboard_list.delete(0, tk.END)

    for item_id, content in db.fetch_all_items():
        clipboard_list.insert(tk.END, content)


def show_manager():
    refresh_clipboard_list()
    root.deiconify()
    root.lift()
    root.focus_force()


def open_manager():
    # The keyboard listener is on a separate thread.
    root.after(0, show_manager)


register_hold(open_manager, 2)
start_clipboard_watcher(root)
root.mainloop()