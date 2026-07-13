import keyboard
import threading

def register_hold(on_hold, hold_time=2.0):
    hold_timer = None
    shortcut_fired = False

    def start_timer():
        nonlocal hold_timer

        if hold_timer is None and not shortcut_fired:
            hold_timer = threading.Timer(hold_time, check_held_keys)
            hold_timer.start()

    def check_held_keys():
        nonlocal hold_timer

        hold_timer = None

        if keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
            on_hold()

    def cancel_timer():
        nonlocal hold_timer

        if hold_timer is not None:
            hold_timer.cancel()
            hold_timer = None
        
        nonlocal shortcut_fired
        shortcut_fired = False

    def handle_key_event(event):
        if event.event_type == 'down' and keyboard.is_pressed('ctrl') and keyboard.is_pressed('shift'):
            start_timer()
        elif event.event_type == 'up' and event.name in ['ctrl', 'shift']:
            cancel_timer()

    keyboard.hook(handle_key_event)