import sqlite3

class DBConnection:
    """
    A class used to manage a connection to a SQLite database.

    Attributes:
    -----------
    db_file : str
        The file path to the SQLite database.
    connection : sqlite3.Connection
        The SQLite connection object. Initially None until connected.

    Methods:
    --------
    __init__(self, db_file: str):
        Initializes the DBConnection with the path to the database file.
    connect(self):
        Establishes a connection to the SQLite database.
    disconnect(self):
        Closes the connection to the SQLite database if it is open.
    execute_query(self, query, params=""):
        Executes a given SQL query on the connected database.
    get_last_row_id(self):
        Returns the row ID of the last row affected by an INSERT operation.
    commit_query(self):
        Commits the current transaction to the database and disconnects.
    create_tables(self):
        Creates the Users, Habits, and CompletionDates tables if they do not exist.
    delete_tables(self):
        Deletes all tables from the database except 'sqlite_sequence'.
    """
    def __init__(self, db_file: str):
        """
        Initializes the DBConnection with the specified database file.

        Parameters:
        -----------
        db_file : str
            The file path to the SQLite database.
        """
        self.db_file = db_file
        self.connection = None

    def connect(self):
        """Establishes a connection to the SQLite database using the db_file path."""
        self.connection = sqlite3.connect(self.db_file)

    def disconnect(self):
        """
        Closes the connection to the SQLite database if it is open and sets the
        connection attribute back to None.
        """
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=""):
        """
        Executes a SQL query using the open connection.

        Parameters:
        -----------
        query : str
            The SQL query to execute.
        params : tuple or str, optional
            Parameters to bind to the SQL query (default is an empty string).

        Returns:
        --------
        sqlite3.Cursor
            The cursor object used to execute the query.
        """
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor

    def get_last_row_id(self):
        """
        Returns the row ID of the last row inserted into the database.

        Returns:
        --------
        int
            The row ID of the last inserted row.
        """
        self.connect()
        cursor = self.connection.cursor()
        return cursor.lastrowid

    def commit_query(self):
        """
        Commits the current transaction to the database and disconnects the connection.
        """
        self.connection.commit()
        self.disconnect()

    def create_tables(self):
        """
        Creates the necessary tables (Users, Habits, CompletionDates) in the database if they do not exist.
        """
        self.connect()
        conn = self.connection
        cursor = conn.cursor()

        # Checking for table existence and creating them if not found
        table_creation_queries = {
            'Users': '''CREATE TABLE Users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        created_at TEXT NOT NULL DEFAULT (strftime('%d-%m-%Y', 'now'))
                    )''',
            'Habits': '''CREATE TABLE Habits (
                        habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        name TEXT NOT NULL,
                        periodicity TEXT NOT NULL,
                        creation_date TEXT NOT NULL DEFAULT (strftime('%d-%m-%Y', 'now')),
                        current_streak INTEGER DEFAULT 0,
                        longest_streak INTEGER DEFAULT 0,
                        FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
                    )''',
            'CompletionDates': '''CREATE TABLE CompletionDates (
                        completion_date_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        habit_id INTEGER,
                        completion_date TEXT NOT NULL DEFAULT (strftime('%d-%m-%Y', 'now')),
                        FOREIGN KEY (habit_id) REFERENCES Habits(habit_id) ON DELETE CASCADE
                    )'''
        }

        for table, creation_query in table_creation_queries.items():
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                cursor.execute(creation_query)

        # Commit changes and disconnect
        self.connection.commit()
        self.disconnect()

    def delete_tables(self):
        """
        Deletes all tables from the database except the 'sqlite_sequence' table.
        """
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                if table[0] != "sqlite_sequence":
                    cursor.execute(f"DROP TABLE {table[0]}")
