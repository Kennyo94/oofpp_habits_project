from datetime import datetime, timedelta
import uuid

class Habit:

    def __init__(self, name: str, periodicity: str, habit_id=uuid.uuid4().int, creation_date=str(datetime.now())[:10], completion_history=[], current_streak=0, longest_streak=0):

        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_history = completion_history
        self.current_streak = current_streak
        self.longest_streak = longest_streak

    def get_habit_id(self):
        return self.habit_id

    def get_name(self):
        return self.name
    
    def get_periodicity(self):
        return self.periodicity
    
    def get_creation_date(self):
        return self.creation_date
    
    def get_completion_history(self):
        return self.completion_history
    
    def get_current_streak(self):
        return self.current_streak
    
    def get_longest_streak(self):
        return self.longest_streak
    
    def set_name(self, name):
        self.name = name

    def set_habit_id(self, habit_id):
        self.habit_id = habit_id
    
    def set_periodicity(self, periodicity):
        self.periodicity = periodicity
    