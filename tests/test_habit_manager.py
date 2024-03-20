import pytest 
from src.db_connection import DBConnection
from src.habit_manager import HabitManager
from src.user_manager import UserManager
from src.models.habit import Habit
from src.models.user import User
import sqlite3



user_1 = User("john_doe", 1, "2023-10-09")
user_2 = User("jane_doe", 2, "2024-01-09")
user_3 = User("max_mustermann", 3, "2024-03-15")

habit1 = Habit("Exercise", "daily", 1, "2023-10-10", ["2023-10-10", "2023-10-11"], 2, 2)
habit2 = Habit("Reading", "daily", 2, "2024-03-02", ["2024-03-02", "2024-03-03", "2024-03-04", "2024-03-05"], 4, 4)
habit3 = Habit("Running", "daily", 3, "2024-03-15", ["2024-03-15", "2024-03-16", "2024-03-17", "2024-03-18", "2024-03-19"], 5, 5)
habit4 = Habit("Meditation", "daily", 4)  # Habit with no completion history
habit5 = Habit("Coding", "weekly", 5, "2024-02-08", ["2024-02-08", "2024-02-13", "2024-02-29", "2024-03-05"], 2, 2)
habit6 = Habit("Walking", "weekly", 6, "2024-02-08", ["2024-02-08", "2024-02-13", "2024-02-23", "2024-02-29"], 4, 4)






@pytest.fixture(scope="class")
def db_manager():
    manager = DBConnection("../db/test_database.db")
    manager.create_tables()
    h_manager = HabitManager(manager)
    u_manager = UserManager(manager)

    u_manager.import_user(user_1)
    u_manager.import_user(user_2)
    u_manager.import_user(user_3)

    h_manager.add_habit(habit1, 1)
    h_manager.add_habit(habit2, 1)
    h_manager.add_habit(habit3, 1)
    h_manager.add_habit(habit4, 3)
    h_manager.add_habit(habit5, 2)
    h_manager.add_habit(habit6, 2)


    yield manager
    manager.delete_tables()

class TestHabitManager:

    def test_habit_creation(self):
        habit = Habit("Exercise", "daily")
        assert habit.get_name() == "Exercise"
        assert habit.get_periodicity() == "daily"
        assert len(habit.get_creation_date()) >= 1
        assert habit.get_completion_history() == []
        assert habit.get_current_streak() == 0
        assert habit.get_longest_streak() == 0


    def test_table_creation(self, db_manager):
        with sqlite3.connect(db_manager.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            assert len(tables) == 4
            table_names = [table[0] for table in tables]
            assert "Users" in table_names and "Habits" in table_names and "CompletionDates" in table_names


        
    def test_get_habits(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habits = habit_manager.get_habits()
        assert len(habits) == 6
        



        




