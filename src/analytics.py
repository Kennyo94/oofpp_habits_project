from src.models.habit import Habit
from src.db_connection import DBConnection
from src.habit_manager import HabitManager
from datetime import datetime
from functools import reduce



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
    Get the dates of the longest streak among all defined habits.

    Args:
        habits (list): A list of habit objects.

    Returns:
        list: A list of dates corresponding to the longest streak.
    """
    # Define a function to compare run streaks and return the habit with the longest streak
    longest_streak_habit = reduce(lambda x, y: x if x.get_longest_streak() >= y.get_longest_streak() else y, habits)

    longest_streak = []
    current_streak = []


    dates = longest_streak_habit.get_completion_history()

    return longest_streak_habit, get_longest_streak_dates(dates)
    

def get_longest_run_streak_for_habit(habit: Habit) -> list:
    """
    Get the list of dates for the longest streak of completions for a given habit.

    Args:
        habit (Habit): The habit object for which to find the longest streak.

    Returns:
        list: A list of dates representing the longest streak of completions.
    """
    completion_history = habit.get_completion_history()
    return get_longest_streak_dates(completion_history)


# Get the list of dates for the longest streak of completions
def get_longest_streak_dates(completion_dates) -> list:
    """
    Find the longest streak of consecutive dates from a list of completion dates.

    Args:
        completion_dates (list): A list of completion dates in string format ('YYYY-MM-DD').

    Returns:
        list: A list of dates representing the longest streak of consecutive completions.
    """
    longest_streak = []
    current_streak = []

    # Iterate through the sorted dates to find the longest streak
    for i in range(len(completion_dates) - 1):
        current_date = completion_dates[i]
        next_date = completion_dates[i + 1]

        # Check if the next date is consecutive
        if (datetime.strptime(next_date, '%Y-%m-%d') - datetime.strptime(current_date, '%Y-%m-%d')).days == 1:
            current_streak.append(current_date)
        else:
            if i-1 > 0 and (datetime.strptime(current_date, '%Y-%m-%d') - datetime.strptime(completion_dates[i-1], '%Y-%m-%d')).days == 1:
                current_streak.append(current_date)
            # Update the longest streak if the current streak is longer
            if len(current_streak) > len(longest_streak):
                longest_streak = current_streak.copy()
            current_streak = []

    # Handle the last streak
    if len(current_streak) > len(longest_streak):
        longest_streak = current_streak.copy()

    # Include the last date in the longest streak if it's part of the streak
    last_date = completion_dates[-1]
    if (datetime.strptime(last_date, '%Y-%m-%d') - datetime.strptime(longest_streak[-1], '%Y-%m-%d')).days == 1:
        longest_streak.append(last_date)

    return longest_streak
