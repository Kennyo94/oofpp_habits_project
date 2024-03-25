from models.habit import Habit
from db_connection import DBConnection
from habit_manager import HabitManager
from datetime import datetime


def get_all_tracked_habits(manager: HabitManager) -> list:
    """
    Retrieve a list of all currently tracked habits.

    Parameters:
    -----------
    manager : HabitManager
        An instance of a habit manager

    Returns:
    --------
    List[Habit]
        A list of Habit objects representing all currently tracked habits.
    """
  
    return manager.get_habits()


def get_habits_by_periodicity(manager: HabitManager, periodicity: str) -> list:
    """
    Return a list of all habits with the same periodicity.

    Parameters:
    -----------
    manager : HabitManager
        An instance of the habit manager.
    periodicity : str
        The periodicity to filter habits by.

    Returns:
    --------
    List[Habit]
        A list of Habit objects with the specified periodicity.
    """
    result = manager.get_habits()
    habits = list(filter(lambda habit: habit.get_periodicity() == periodicity, result))
    return habits


def get_longest_run_streak_all_habits(habits: list) -> int:
    """
    Return the longest run streak of all defined habits.

    Parameters:
    -----------
    habits : List[Habit]
        A list of Habit objects.

    Returns:
    --------
    int
        The longest run streak of all habits.
    """
    sorted_habits = sorted(habits, key=lambda habit: habit.get_longest_streak(), reverse=True)
    return sorted_habits[0].get_longest_streak()




db = DBConnection("../db/habit_tracker.db")
manager = HabitManager(db)

habits = get_all_tracked_habits(manager)
print(get_longest_run_streak_all_habits(habits))
