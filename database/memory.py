import sqlite3

class DatabaseInterface:
    def __init__(self, db_name='app_data.db'):
        """Initialize the database interface and create a connection."""
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self._initialize_database()

    def _initialize_database(self):
        """Set up the database schema if it doesn't exist."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE NOT NULL,
                value TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def insert_or_update(self, key, value):
        """Insert a new record or update an existing one."""
        self.cursor.execute('''
            INSERT INTO records (key, value)
            VALUES (?, ?)
            ON CONFLICT(key) DO UPDATE SET value=excluded.value
        ''', (key, value))
        self.conn.commit()

    def retrieve(self, key):
        """Retrieve the value associated with a given key."""
        self.cursor.execute('SELECT value FROM records WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def delete(self, key):
        """Delete a record by its key."""
        self.cursor.execute('DELETE FROM records WHERE key = ?', (key,))
        self.conn.commit()

    def get_all_records(self):
        """Retrieve all records from the database."""
        self.cursor.execute('SELECT key, value FROM records')
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
