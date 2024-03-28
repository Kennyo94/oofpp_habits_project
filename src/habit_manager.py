from src.models.habit import Habit
from datetime import datetime, timedelta
from src.exceptions import HabitNotFoundException, HabitAlreadyExistsException, InvalidPeriodicityException


class HabitManager:
    """
    A class to manage habits within a database.

    Attributes:
    -----------
    db : DBConnection
        The database connection object used to interact with the database.

    Methods:
    --------
    __init__(self, dbconnection):
        Initializes the HabitManager with a database connection.
    get_habits(self):
        Retrieves all habits from the database.
    get_habit_by_id(self, habit_id):
        Retrieves a habit from the database by its unique identifier.
    get_habit_by_name(self, name):
        Retrieves a habit from the database by its name.
    get_habits_from_user(self, user_id):
        Retrieves all habits associated with a particular user from the database.
    get_habit_from_user_by_id(self, user_id, habit_id):
        Retrieves a habit associated with a particular user by its unique identifier.
    add_habit(self, habit: Habit, user_id):
        Adds a new habit to the database for a specific user.
    add_habit_by_info(self, name, periodicity, user_id):
        Adds a new habit to the database for a specific user by its name and perdiocitiy.
    delete_habit(self, habit_id):
        Deletes a habit from the database by its unique identifier.
    update_habit_name(self, habit_id, new_name):
        Updates the name of a habit in the database.
    update_habit_periodicity(self, habit_id, periodicity):
        Updates the periodicity of a habit in the database.
    update_streak(self, habit_id, new_current, new_longest):
        Updates the streak of a habit in the database.
    complete_habit(self, habit_id, date):
        Marks a habit as completed for a particular date in the database.
    """

    def __init__(self, dbconnection):
        """
        Constructs a HabitManager object with a database connection.

        Parameters:
        -----------
        dbconnection : DBConnection
            The database connection object to be used for interacting with the database.
        """
        self.db = dbconnection

    def get_habits(self) -> list:
        """
        Retrieves all habits from the database.

        Returns:
        --------
        list
            A list of Habit objects representing all habits stored in the database.
        """
        habits = []
        query = "SELECT * FROM Habits"
        result = self.db.execute_query(query).fetchall()

        if result is not None:
            for habit in result:
                habit_id = habit[0]
                completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
                cd = self.db.execute_query(completion_query, (habit_id, )).fetchall()
                completion_dates = [str(dates[0]) for dates in cd]
                h = Habit(habit[2], habit[3], habit[0], habit[4], completion_dates, habit[5], habit[6])
                habits.append(h)
            return habits
        return []

    def get_habit_by_id(self, habit_id) -> Habit:
        """
        Retrieves a habit from the database by its unique identifier.

        Parameters:
        -----------
        habit_id : int
            The unique identifier of the habit to retrieve.

        Returns:
        --------
        Habit or None
            A Habit object representing the retrieved habit if found, otherwise None.
        
        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id is found in the database.
        """
        query = "SELECT * FROM Habits WHERE habit_id = ?"
        result = self.db.execute_query(query, (habit_id, )).fetchone()

        if result:
            completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
            cd = self.db.execute_query(completion_query, (result[0], )).fetchall()
            completion_dates = [str(dates[0]) for dates in cd]
            return Habit(result[2], result[3], result[0], result[4], completion_dates, result[5], result[6])
        else:
            raise HabitNotFoundException(habit_id)


    
    def get_habit_by_name(self, name) -> Habit:
        """
        Retrieves a habit from the database by its name.

        Parameters:
        -----------
        name : str
            The name of the habit to retrieve.

        Returns:
        --------
        Habit or None
            A Habit object representing the retrieved habit if found, otherwise None.
        """
        query = "SELECT * FROM Habits WHERE name = ?"
        result = self.db.execute_query(query, (name, )).fetchone()

        if result:
            completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
            cd = self.db.execute_query(completion_query, (result[0], )).fetchall()
            completion_dates = [str(dates[0]) for dates in cd]
            return Habit(result[2], result[3], result[0], result[4], completion_dates, result[5], result[6])
        else:
            return None

    

    def get_habits_from_user(self, user_id) -> list:
        """
        Retrieves all habits associated with a particular user from the database.

        Parameters:
        -----------
        user_id : int
            The unique identifier of the user whose habits are to be retrieved.

        Returns:
        --------
        list
            A list of Habit objects representing the habits associated with the specified user.
        """
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
    
    def get_habit_from_user_by_id(self, user_id, habit_id) -> Habit:
        """
        Retrieves a habit associated with a particular user by its unique identifier.

        Parameters:
        -----------
        user_id : int
            The unique identifier of the user.
        habit_id : int
            The unique identifier of the habit to retrieve.

        Returns:
        --------
        Habit or None
            A Habit object representing the retrieved habit if found, otherwise None.
        
        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id associated with the specified user_id is found in the database.
        """
        query = "SELECT * FROM Habits WHERE user_id = ? AND habit_id = ?"
        result = self.db.execute_query(query, (user_id, habit_id, )).fetchone()

        if result:
            completion_query = "SELECT completion_date FROM CompletionDates WHERE habit_id = ?"
            cd = self.db.execute_query(completion_query, (result[0], )).fetchall()
            completion_dates = [str(dates[0]) for dates in cd]
            return Habit(result[2], result[3], result[0], result[4], completion_dates, result[5], result[6])
        else:
            raise HabitNotFoundException(habit_id)
        

    def add_habit(self, habit: Habit, user_id):
        """
        Adds a new habit to the database for a specific user.

        Parameters:
        -----------
        habit : Habit
            The Habit object representing the habit to be added.
        user_id : int
            The unique identifier of the user associated with the new habit.

        Raises:
        -------
        HabitAlreadyExistsException
            If a habit with the same name already exists for the specified user.
        """
        name = habit.get_name()
        periodicity = habit.get_periodicity()
        creation_date = habit.get_creation_date()
        current_streak = habit.get_current_streak()
        longest_streak = habit.get_longest_streak()
        completion_dates = habit.get_completion_history()

        habit_to_be_added = self.get_habit_by_name(name)
        habit_user_id = self.db.execute_query("SELECT user_id FROM Habits WHERE name = ? AND periodicity = ? AND creation_date = ? AND current_streak = ? AND longest_streak = ?", (name, periodicity, creation_date, current_streak, longest_streak, )).fetchone()


        if habit_to_be_added is None or (user_id is not habit_user_id and habit_to_be_added is not None):
            query = "INSERT INTO Habits (user_id, name, periodicity, creation_date, current_streak, longest_streak) VALUES (?, ?, ?, ?, ?, ?)"
            self.db.execute_query(query, (user_id, name, periodicity, creation_date, current_streak, longest_streak))
            self.db.commit_query()

            habit_query = "SELECT habit_id FROM Habits WHERE user_id = ? AND name = ? AND periodicity = ? AND creation_date = ? AND current_streak = ? AND longest_streak = ?"
            habit_id = self.db.execute_query(habit_query, (user_id, name, periodicity, creation_date, current_streak, longest_streak)).fetchone()[0]

            for date in completion_dates:
                query = "INSERT INTO CompletionDates (habit_id, completion_date) VALUES (?, ?)"
                self.db.execute_query(query, (habit_id, date))
                self.db.commit_query()
        else:
            raise HabitAlreadyExistsException(name)



    def add_habit_by_info(self, name, periodicity, user_id):
        """
        Create and add a new habit to the habit manager based on provided information.

        Parameters:
            name (str): The name of the habit.
            periodicity (str): The periodicity of the habit ('daily' or 'weekly').
            user_id (int): The ID of the user associated with the habit.

        """
        habit = Habit(name, periodicity)
        self.add_habit(habit, user_id)

    def delete_habit(self, habit_id) -> Habit:
        """
        Deletes a habit from the database by its unique identifier.

        Parameters:
        -----------
        habit_id : int
            The unique identifier of the habit to be deleted.

        Returns:
        --------
        Habit
            The Habit object representing the deleted habit.

        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id is found in the database.
        """
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
            raise HabitNotFoundException(habit_id)
        

    def update_habit_name(self, habit_id, new_name):
        """
        Updates the name of a habit in the database.

        Parameters:
        -----------
        habit_id : int
            The unique identifier of the habit to be updated.
        new_name : str
            The new name to assign to the habit.

        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id is found in the database.
        """
        habit_to_be_updated = self.get_habit_by_id(habit_id)

        if habit_to_be_updated is not None:
            query = "UPDATE Habits SET name = ? WHERE habit_id = ?"
            self.db.execute_query(query, (new_name, habit_id, ))
            self.db.commit_query()
            return

        if habit_to_be_updated is None:
            raise HabitNotFoundException(habit_id)
        
       

    def update_habit_periodicity(self, habit_id, periodicity):
        """
        Updates the periodicity of a habit in the database.

        Parameters:
        -----------
        habit_id : int
            The unique identifier of the habit to be updated.
        periodicity : str
            The new periodicity to assign to the habit.

        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id is found in the database.
        """
        habit_to_be_updated = self.get_habit_by_id(habit_id)

        if habit_to_be_updated is not None:
            query = "UPDATE Habits SET periodicity = ? WHERE habit_id = ?"
            self.db.execute_query(query, (periodicity, habit_id, ))
            self.db.commit_query()
            return

        if habit_to_be_updated is None:
            raise HabitNotFoundException(habit_id)
            

    def update_streak(self, habit_id, new_current, new_longest):
        """
        Updates the streak of a habit in the database.

        Parameters:
        -----------
        habit_id : int
            The unique identifier of the habit whose streak is to be updated.
        new_current : int
            The new current streak value.
        new_longest : int
            The new longest streak value.

        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id is found in the database.
        """
        query = "UPDATE Habits SET current_streak = ?, longest_streak = ? WHERE habit_id = ?"
        self.db.execute_query(query, (new_current, new_longest, habit_id, ))
        self.db.commit_query()



    def complete_habit(self, habit_id, date):
        """
        Marks a habit as completed for a particular date in the database. It also updates the streak accordingly.

        Parameters:
        -----------
        habit_id : int
            The unique identifier of the habit to mark as completed.
        date : str
            The date when the habit was completed in 'YYYY-MM-DD' format.

        Raises:
        -------
        HabitNotFoundException
            If no habit with the given habit_id is found in the database.
        """
        habit_to_be_completed = self.get_habit_by_id(habit_id)

        if habit_to_be_completed is not None:
            if len(habit_to_be_completed.get_completion_history()) == 0:
                new_current = 1
                new_longest = max(new_current, habit_to_be_completed.get_longest_streak())
                self.update_streak(habit_id, 1, 1)
            else:

                last_completion_date = datetime.strptime(habit_to_be_completed.get_completion_history()[-1], "%Y-%m-%d")
                current_completion_date = datetime.strptime(str(date)[:10], "%Y-%m-%d")

                if habit_to_be_completed.get_periodicity() == "daily":
                    if current_completion_date - last_completion_date == timedelta(days=1):
                        new_current = habit_to_be_completed.get_current_streak() + 1
                        new_longest = max(new_current, habit_to_be_completed.get_longest_streak())
                        self.update_streak(habit_id, new_current, new_longest)
                    else:
                        self.update_streak(habit_id, 1, max(1, habit_to_be_completed.get_longest_streak()))

                elif habit_to_be_completed.get_periodicity() == "weekly":

                    next_week_start = last_completion_date + timedelta(days=(7 - last_completion_date.weekday()))
                    next_week_end = next_week_start + timedelta(days=6)

                    if current_completion_date >= next_week_start and current_completion_date <= next_week_end:
                        new_current = habit_to_be_completed.get_current_streak() + 1
                        new_longest = max(new_current, habit_to_be_completed.get_longest_streak())
                        self.update_streak(habit_id, new_current, new_longest)

                    else:
                        self.update_streak(habit_id, 1, max(1, habit_to_be_completed.get_longest_streak()))

                else:
                    raise InvalidPeriodicityException(habit_to_be_completed.get_periodicity())
                
            query = "INSERT INTO CompletionDates (habit_id, completion_date) VALUES (?,?)"
            date_to_be_inserted = str(date)[:10]
            self.db.execute_query(query, (habit_id, date_to_be_inserted, ))
            self.db.commit_query()
        
        else:
            raise HabitNotFoundException(habit_id)




