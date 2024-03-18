from models.habit import Habit
from db_connection import DBConnection


class HabitManager:

    def __init__(self, dbconnection):
        self.db = dbconnection

    def get_habits(self):
        habits = []
        query = "SELECT * FROM Habits"
        result = self.db.execute_query(query).fetchall()
        
        if result is not None:
            for habit in result:
                habit_id = habit[0]
                completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
                cd = self.db.execute_query(completion_query, (habit_id, )).fetchall()
                completion_dates = [str(dates[0]) for dates in cd]
                h = Habit(habit[2],habit[3], habit[0], habit[4], completion_dates, habit[5], habit[6])
                habits.append(h)

            return habits
        
        return []




db = DBConnection("../db/habit_tracker.db")
h_manager = HabitManager(db)

print(h_manager.get_habits())