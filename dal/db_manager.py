import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="shot_timer.db"):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        """Connect to the SQLite database. Creates the file if it doesn't exist."""
        if not os.path.exists(self.db_name):
            print(f"Database {self.db_name} not found. Creating a new one.")
        self.connection = sqlite3.connect(self.db_name)

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    def execute_query(self, query, params=None):
        """Execute a single query."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def execute_many(self, query, params_list):
        """Execute a query with multiple parameters."""
        with self.connection:
            cursor = self.connection.cursor()
            cursor.executemany(query, params_list)

    def cursor(self):
        return self.connection.cursor()
