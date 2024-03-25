from src.habit_click import cli
from src.analytics import *
from src.habit_manager import HabitManager
from src.db_connection import DBConnection


db = DBConnection("db/habit_tracker.db")
h = HabitManager(db)




if __name__ == "__main__":
    cli()