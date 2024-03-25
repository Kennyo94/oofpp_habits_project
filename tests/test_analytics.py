import pytest 
from src.db_connection import DBConnection
from src.habit_manager import HabitManager
from src.user_manager import UserManager
from src.models.habit import Habit
from src.models.user import User
from src.exceptions import HabitNotFoundException
from datetime import datetime
from src.analytics import *
import sqlite3


user_1 = User("john_doe", 1, "2023-10-09")
habit1 = Habit("Running", "daily", 1, "2024-03-01", ['2024-03-01', '2024-03-02', '2024-03-03', '2024-03-04', '2024-03-05', '2024-03-07' ,'2024-03-10', '2024-03-11', '2024-03-12', '2024-03-13', '2024-03-14', '2024-03-15', '2024-03-16'], 7, 7)
habit2 = Habit("Coding", "weekly", 2, "2024-02-08", ["2024-02-08", "2024-02-13", "2024-02-29", "2024-03-05"], 2, 2)
habit3 = Habit("Exercise", "daily", 3, "2023-10-10", ["2023-10-10", "2023-10-11", '2024-03-01', '2024-03-02', '2024-03-03', '2024-03-10', '2024-03-11'], 2, 3)


@pytest.fixture(scope="class")
def db_manager():
    manager = DBConnection("../db/test_database.db")
    manager.create_tables()
    h_manager = HabitManager(manager)
    u_manager = UserManager(manager)

    u_manager.import_user(user_1)
    h_manager.add_habit(habit1, 1)
    h_manager.add_habit(habit2, 1)
    h_manager.add_habit(habit3, 1)


    yield manager
    manager.delete_tables()



class TestAnalytics:
    

    def test_get_all_tracked_habits(self, db_manager):
        manager = HabitManager(db_manager)
        habits = get_all_tracked_habits(manager)
        assert habits is not None
        assert len(habits) == 3

    def test_get_habits_by_periodicity(self, db_manager):
        manager = HabitManager(db_manager)
        daily_habits = get_habits_by_periodicity(manager, "daily")
        weekly_habits = get_habits_by_periodicity(manager, "weekly")
        assert len(daily_habits) == 2
        assert len(weekly_habits) == 1


    def test_get_longest_run_streak_all_habits(self, db_manager):
        manager = HabitManager(db_manager)
        habits = get_all_tracked_habits(manager)
        streak_dates = get_longest_run_streak_all_habits(habits)[1]
        assert len(streak_dates) == 7


    def test_get_longset_run_streak_for_habit(self, db_manager):
        manager = HabitManager(db_manager)
        habit = manager.get_habit_by_id(3)
        streak_dates = get_longest_run_streak_for_habit(habit)
        assert len(streak_dates) == 3


