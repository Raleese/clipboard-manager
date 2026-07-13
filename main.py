import keyboard
import threading
import tkinter as tk

hold_timer = None
shortcut_fired = False

def open_manager():
    global shortcut_fired
    shortcut_fired = True

    print("Opened")

    root = tk.Tk()
    root.title("Clipboard Manager")
    root.mainloop()

def start_timer():
    global hold_timer

    if hold_timer is None and not shortcut_fired:
        hold_timer = threading.Timer(2.0, check_held_keys)
        hold_timer.start()

def check_held_keys():
    global hold_timer

    hold_timer = None

    if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
        open_manager()

def cancel_timer():
    global hold_timer

    if hold_timer is not None:
        hold_timer.cancel()
        hold_timer = None
    
    shortcut_fired = False

def handle_key_event(event):
    if event.event_type == 'down' and keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
        start_timer()
    elif event.event_type == 'up' and event.name in ['ctrl', 'shift']:
        cancel_timer()

keyboard.hook(handle_key_event)
keyboard.wait()