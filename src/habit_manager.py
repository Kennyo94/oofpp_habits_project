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
    
    def get_habit_by_id(self, habit_id):
        query = "SELECT * FROM Habits WHERE habit_id = ?"
        result = self.db.execute_query(query, (habit_id, )).fetchone()

        if result:
            completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
            cd = self.db.execute_query(completion_query, (result[0], )).fetchall()
            completion_dates = [str(dates[0]) for dates in cd]
            return Habit(result[2], result[3], result[0], result[4], completion_dates, result[5], result[6])

        return None
    
    def get_habit_by_name(self, name):
        query = "SELECT * FROM Habits WHERE name = ?"
        result = self.db.execute_query(query, (name, )).fetchone()

        if result:
            completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
            cd = self.db.execute_query(completion_query, (result[0], )).fetchall()
            completion_dates = [str(dates[0]) for dates in cd]
            return Habit(result[2], result[3], result[0], result[4], completion_dates, result[5], result[6])

        return None
    

    def get_habits_from_user(self, user_id):
        habits = []
        query = "SELECT * FROM Habits WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id, )).fetchall()

        if result:
            for habit in result:
                habit_id = habit[0]
                completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
                cd = self.db.execute_query(completion_query, (habit_id, )).fetchall()
                completion_dates = [str(dates[0]) for dates in cd]
                h = Habit(habit[2],habit[3], habit[0], habit[4], completion_dates, habit[5], habit[6])
                habits.append(h)
            return habits
        
        return []
    
    def get_habit_from_user_by_id(self, user_id, habit_id):
        query = "SELECT * FROM Habits WHERE user_id = ? AND habit_id = ?"
        result = self.db.execute_query(query, (user_id, habit_id, )).fetchone()

        if result:
            completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
            cd = self.db.execute_query(completion_query, (result[0], )).fetchall()
            completion_dates = [str(dates[0]) for dates in cd]
            return Habit(result[2], result[3], result[0], result[4], completion_dates, result[5], result[6])

        return None


    def add_habit(self, habit: Habit, user_id):

        name = habit.get_name()
        periodicity = habit.get_periodicity()
        creation_date = habit.get_creation_date()
        current_streak = habit.get_current_streak()
        longest_streak = habit.get_longest_streak()
        completion_dates = habit.get_completion_history()

        habit_to_be_added = self.get_habit_by_name(name)

        if habit_to_be_added is None:
            query = "INSERT INTO Habits (user_id, name, periodicity, creation_date, current_streak, longest_streak) VALUES (?, ?, ?, ?, ?, ?)"
            self.db.execute_query(query, (user_id, name, periodicity, creation_date, current_streak, longest_streak))
            self.db.commit_query()

            habit_query = "SELECT habit_id FROM Habits WHERE user_id = ? AND name = ? AND periodicity = ? AND creation_date = ? AND current_streak = ? AND longest_streak = ?"
            habit_id = self.db.execute_query(habit_query, (user_id, name, periodicity, creation_date, current_streak, longest_streak)).fetchone()[0]
            print(habit_id)

            for date in completion_dates:
                query = "INSERT INTO CompletionDates (habit_id, completion_date) VALUES (?, ?)"
                self.db.execute_query(query, (habit_id, date))
                self.db.commit_query()
        else:
            raise ValueError("Habit Already Exists!")



    def delete_habit(self, habit_id):
        habit_to_be_deleted = self.get_habit_by_id(habit_id)
        if habit_to_be_deleted is not None:
            query = "DELETE FROM Habits WHERE habit_id = ?"
            self.db.execute_query(query, (habit_id, ))
            self.db.commit_query()
            completion_query = "DELETE FROM CompletionDates WHERE habit_id = ?"
            self.db.execute_query(completion_query, (habit_id, ))
            self.db.commit_query()

            return habit_to_be_deleted

        else:
            raise ValueError("Habit Not Found!")
        


    


db = DBConnection("../db/habit_tracker.db")

h_manager = HabitManager(db)

habit = Habit("Cooking", "daily", completion_history=["2024-03-01","2024-03-02", "2024-03-03"], current_streak=0, longest_streak=3)


h_manager.delete_habit(51)
