import sqlite3

class DBConnection:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=""):
        self.connect()
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        return cursor
    
    def commit_query(self):
        self.connection.commit()
        self.disconnect()
    
    def create_tables(self):
        # Connect to the database
        self.connect()
        conn = self.connection
        cursor = conn.cursor()

        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users'")
        users_table_exists = cursor.fetchone()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Habits'")
        habits_table_exists = cursor.fetchone()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='CompletionDates'")
        completion_dates_table_exists = cursor.fetchone()


        #DELETE THIS ONE WHEN WE'RE DONE! JUST TO CHECK
        if users_table_exists or habits_table_exists or completion_dates_table_exists:
            print("Tables Already Exist!")
            return 

        # Create tables if they don't exist
        if not users_table_exists:
            cursor.execute('''CREATE TABLE Users (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                created_at TEXT NOT NULL DEFAULT (strftime('%d-%m-%Y', 'now'))
                            )''')

        if not habits_table_exists:
            cursor.execute('''CREATE TABLE Habits (
                                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                name TEXT NOT NULL,
                                periodicity TEXT NOT NULL,
                                creation_date TEXT NOT NULL DEFAULT (strftime('%d-%m-%Y', 'now')),
                                current_streak INTEGER DEFAULT 0,
                                longest_streak INTEGER DEFAULT 0,
                                FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
                            )''')

        if not completion_dates_table_exists:
            cursor.execute('''CREATE TABLE CompletionDates (
                                completion_date_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                habit_id INTEGER,
                                completion_date TEXT NOT NULL DEFAULT (strftime('%d-%m-%Y', 'now')),
                                FOREIGN KEY (habit_id) REFERENCES Habits(habit_id) ON DELETE CASCADE
                            )''')

        # Commit changes and close connection
        self.connection.commit()
        self.disconnect()
    