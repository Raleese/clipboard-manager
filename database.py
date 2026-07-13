import sqlite3

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clipboard_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                content TEXT NOT NULL
            )''')
        self.connection.commit()
    
    def insert_item(self, content):
        self.cursor.execute('INSERT INTO clipboard_history (content) VALUES (?)', (content,))
        self.connection.commit()

    def fetch_all_items(self):
        self.cursor.execute('SELECT id, content FROM clipboard_history ORDER BY id DESC')
        return self.cursor.fetchall()
    
    def delete_oldest_item(self):
        self.cursor.execute('DELETE FROM clipboard_history WHERE id = (SELECT MIN(id) FROM clipboard_history)')
        self.connection.commit()

    def get_count(self):
        self.cursor.execute('SELECT COUNT(*) FROM clipboard_history')
        return self.cursor.fetchone()[0]
