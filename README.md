Clipboard Manager

Clipboard Manager is a small Windows clipboard history app. It watches copied text, stores the most recent entries in a local SQLite database, and opens a simple Tk window when you hold `Ctrl + Shift`.

Features

- Watches clipboard text in the background
- Stores the latest copied text entries locally
- Opens the history window near the mouse cursor
- Keeps the app running after you close the window

Requirements

- Windows
- Python 3.10+ recommended
- `pyperclip`
- `keyboard`

Install

```powershell
python -m pip install -r requirements.txt
```

Run

```powershell
python main.py
```

Usage

1. Start the app.
2. Copy some text.
3. Hold `Ctrl + Shift` for about half a second.
4. The clipboard history window appears near your cursor.

Notes

- The app stores its database in `%LOCALAPPDATA%\ClipboardManager\clipboard_history.db`.
- The history limit is currently set to 5 items in `main.py`.
- If hotkeys do not work, try running the app as Administrator.

Build a Windows EXE

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

Build the executable:

```powershell
pyinstaller --onefile --windowed --name ClipboardManager main.py
```

The final executable will be in `dist\ClipboardManager.exe`.

Project Layout

- `main.py` - app startup, window handling, and wiring
- `clipboard.py` - clipboard polling and saving
- `hotkeys.py` - global hotkey hold detection
- `database.py` - SQLite storage helpers
