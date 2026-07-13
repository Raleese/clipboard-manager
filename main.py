import tkinter as tk
from hotkeys import register_hold

root = tk.Tk()
root.title("Clipboard Manager")
root.withdraw()  # Hide the main window

def open_manager():
    root.deiconify()  # Show the main window
    root.lift()  # Bring the window to the front
    root.focus_force()  # Focus on the window


register_hold(open_manager, 2)
root.mainloop()