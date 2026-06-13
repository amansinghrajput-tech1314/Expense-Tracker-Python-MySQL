import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG

class DatabaseConnection:
    """Manages low-level database operations using Context Management."""
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor(dictionary=True)
            return self
        except Error as e:
            print(f"\n[!] Database Connection Error: {e}")
            raise e

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()  # Rollback transaction on failure
            else:
                self.conn.commit()
            self.conn.close()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()