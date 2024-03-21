from datetime import datetime
import uuid

class Habit:
    """
    A class to represent a habit.

    Attributes:
    -----------
    habit_id : int
        Unique identifier for the habit, defaults to a UUID converted to integer.
    name : str
        Name of the habit.
    periodicity : str
        The frequency with which the habit should be performed.
    creation_date : str
        The date when the habit was created, defaults to the current date.
    completion_history : list
        A list of dates when the habit was completed.
    current_streak : int
        The current number of consecutive days the habit has been completed.
    longest_streak : int
        The longest number of consecutive days the habit has been completed.

    Methods:
    --------
    __init__(self, name: str, periodicity: str, habit_id=uuid.uuid4().int, creation_date=str(datetime.now())[:10], completion_history=[], current_streak=0, longest_streak=0):
        Initializes the Habit object with name, periodicity, and optional habit_id, creation_date, completion_history, current_streak, and longest_streak.
    get_habit_id(self):
        Returns the habit's unique identifier.
    get_name(self):
        Returns the name of the habit.
    get_periodicity(self):
        Returns the habit's periodicity.
    get_creation_date(self):
        Returns the date the habit was created.
    get_completion_history(self):
        Returns a list of dates when the habit was completed.
    get_current_streak(self):
        Returns the current streak of habit completion.
    get_longest_streak(self):
        Returns the longest streak of habit completion.
    set_name(self, name):
        Sets a new name for the habit.
    set_habit_id(self, habit_id):
        Sets a new unique identifier for the habit.
    set_periodicity(self, periodicity):
        Sets a new periodicity for the habit.
    __str__(self):
        Returns a string representation of the Habit object.
    """
    def __init__(self, name: str, periodicity: str, habit_id=uuid.uuid4().int, creation_date=str(datetime.now())[:10], completion_history=[], current_streak=0, longest_streak=0):
        """
        Constructs all the necessary attributes for the Habit object.

        Parameters:
        -----------
        name : str
            Name of the habit.
        periodicity : str
            The frequency with which the habit should be performed.
        habit_id : int, optional
            Unique identifier for the habit (default is a new UUID as integer).
        creation_date : str, optional
            The date when the habit was created (default is the current date).
        completion_history : list, optional
            A list of dates when the habit was completed (default is empty).
        current_streak : int, optional
            The current number of consecutive days the habit has been completed (default is 0).
        longest_streak : int, optional
            The longest number of consecutive days the habit has been completed (default is 0).
        """
        self.habit_id = habit_id
        self.name = name
        self.periodicity = periodicity
        self.creation_date = creation_date
        self.completion_history = completion_history
        self.current_streak = current_streak
        self.longest_streak = longest_streak

    def get_habit_id(self):
        """Returns the unique identifier of the habit."""
        return self.habit_id

    def get_name(self):
        """Returns the name of the habit."""
        return self.name
    
    def get_periodicity(self):
        """Returns the habit's periodicity."""
        return self.periodicity
    
    def get_creation_date(self):
        """Returns the date the habit was created."""
        return self.creation_date
    
    def get_completion_history(self):
        """Returns a list of dates when the habit was completed."""
        return self.completion_history
    
    def get_current_streak(self):
        """Returns the current streak of habit completion."""
        return self.current_streak
    
    def get_longest_streak(self):
        """Returns the longest streak of habit completion."""
        return self.longest_streak
    
    def set_name(self, name):
        """
        Sets a new name for the habit.

        Parameters:
        -----------
        name : str
            The new name of the habit.
        """
        self.name = name

    def set_habit_id(self, habit_id):
        """
        Sets a new unique identifier for the habit.

        Parameters:
        -----------
        habit_id : int
            The new unique identifier for the habit.
        """
        self.habit_id = habit_id
    
    def set_periodicity(self, periodicity):
        """
        Sets a new periodicity for the habit.

        Parameters:
        -----------
        periodicity : str
            The new frequency with which the habit should be performed.
        """
        self.periodicity = periodicity
    
    def __str__(self):
        """
        Returns a string representation of the Habit object, detailing its attributes.
        """
        return f"Habit ID: {self.habit_id}\nName: {self.name}\nPeriodicity: {self.periodicity}\nCreation Date: {self.creation_date}\nCurrent Streak: {self.current_streak}\nLongest Streak: {self.longest_streak}\nCompletion Dates: {self.completion_history}\n"
