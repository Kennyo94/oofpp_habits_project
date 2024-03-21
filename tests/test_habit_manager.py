import pytest 
from src.db_connection import DBConnection
from src.habit_manager import HabitManager
from src.user_manager import UserManager
from src.models.habit import Habit
from src.models.user import User
from src.exceptions import HabitNotFoundException
from datetime import datetime
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

    
    def test_get_habit(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit = habit_manager.get_habit_by_id(1)
        assert habit.get_habit_id() == habit1.get_habit_id()

    def test_get_habit_not_found(self, db_manager):
        habit_manager = HabitManager(db_manager)
        with pytest.raises(HabitNotFoundException):
            habit_manager.get_habit_by_id(200)


    def test_get_habit_by_name(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit = habit_manager.get_habit_by_name("Coding")
        assert habit.get_habit_id() == habit5.get_habit_id()

    
    def test_get_habit_by_name_not_found(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit = habit_manager.get_habit_by_name("Not a Habit")
        assert habit == None


    def test_get_habits_from_user(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habits = habit_manager.get_habits_from_user(1)
        assert len(habits) == 3

    def test_get_habit_from_user_by_id(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit = habit_manager.get_habit_from_user_by_id(1,1)
        assert habit.get_habit_id() == habit1.get_habit_id()

    
    def test_get_habit_from_user_by_id_not_found(self, db_manager):
        habit_manager = HabitManager(db_manager)
        with pytest.raises(HabitNotFoundException):
            habit_manager.get_habit_from_user_by_id(1,20)

    def test_add_habit(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit = Habit("Test Habit", "daily", 7)
        habit_manager.add_habit(habit, 1)
        assert habit_manager.get_habit_by_id(7).get_habit_id() == habit.get_habit_id()

    
    def test_delete_habit(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit = Habit("Test Habit", "daily", 7)
        habit_manager.add_habit(habit, 1)
        habit_manager.delete_habit(7)
        with pytest.raises(HabitNotFoundException):
            habit_manager.get_habit_by_id(7)


    def test_update_name(self, db_manager):
        habit_manager = HabitManager(db_manager)
        assert habit_manager.get_habit_by_id(1).get_name() == "Exercise"
        habit_manager.update_habit_name(1, "TestUpdate")
        assert habit_manager.get_habit_by_id(1).get_name() == "TestUpdate"

    
    def test_update_periodicity(self, db_manager):
        habit_manager = HabitManager(db_manager)
        assert habit_manager.get_habit_by_id(1).get_periodicity() == "daily"
        habit_manager.update_habit_periodicity(1, "weekly")
        assert habit_manager.get_habit_by_id(1).get_periodicity() == "weekly"


    def test_complete_habit(self, db_manager):
        habit_manager = HabitManager(db_manager)
        habit_manager.complete_habit(4, datetime.now())
        assert habit_manager.get_habit_by_id(4).get_current_streak() == 1
        assert habit_manager.get_habit_by_id(4).get_longest_streak() == 1
        assert len(habit_manager.get_habit_by_id(4).get_completion_history()) == 1


    def test_update_streak_daily(self, db_manager):
        habit_manager = HabitManager(db_manager)
        march_20 = datetime(2024, 3, 20)
        habit_manager.complete_habit(3, march_20)
        assert habit_manager.get_habit_by_id(3).get_current_streak() == 6
        assert habit_manager.get_habit_by_id(3).get_longest_streak() == 6

    def test_update_streak_broken_daily(self, db_manager):
        habit_manager = HabitManager(db_manager)
        march_20 = datetime(2024, 3, 20)
        habit_manager.complete_habit(2, march_20)
        assert habit_manager.get_habit_by_id(2).get_current_streak() == 1
        assert habit_manager.get_habit_by_id(2).get_longest_streak() == 4


    def test_update_streak_weekly(self, db_manager):
        habit_manager = HabitManager(db_manager)
        march_6 = datetime(2024, 3, 6)
        habit_manager.complete_habit(6, march_6)
        assert habit_manager.get_habit_by_id(6).get_current_streak() == 5
        assert habit_manager.get_habit_by_id(6).get_longest_streak() == 5


    def test_update_streak_broken_weekly(self, db_manager):
        habit_manager = HabitManager(db_manager)
        march_20 = datetime(2024, 3, 20)
        habit_manager.complete_habit(5, march_20)
        assert habit_manager.get_habit_by_id(5).get_current_streak() == 1
        assert habit_manager.get_habit_by_id(5).get_longest_streak() == 2










    










        



        




