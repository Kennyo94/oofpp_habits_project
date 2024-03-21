
class HabitNotFoundException(Exception):
    """
    Exception raised when a habit is not found.

    Attributes:
    -----------
    habit_id : int
        The ID of the habit that was not found.
    message : str
        A descriptive message indicating that the habit with the specified ID was not found.

    Methods:
    --------
    __init__(self, habit_id):
        Initializes the exception with the provided habit ID and constructs the error message.
    """
    def __init__(self, habit_id):
        """
        Initializes the HabitNotFoundException with the provided habit ID.

        Parameters:
        -----------
        habit_id : int
            The ID of the habit that was not found.
        """
        self.habit_id = habit_id
        self.message = f"Habit with ID {self.habit_id} not found"
        super().__init__(self.message)


class HabitAlreadyExistsException(Exception):
    """
    Exception raised when attempting to create a habit that already exists.

    Attributes:
    -----------
    habit_name : str
        The name of the habit that already exists.
    message : str
        A descriptive message indicating that a habit with the specified name already exists.

    Methods:
    --------
    __init__(self, habit_name):
        Initializes the exception with the provided habit name and constructs the error message.
    """
    def __init__(self, habit_name):
        """
        Initializes the HabitAlreadyExistsException with the provided habit name.

        Parameters:
        -----------
        habit_name : str
            The name of the habit that already exists.
        """
        self.habit_name = habit_name
        self.message = f"Habit '{self.habit_name}' already exists"
        super().__init__(self.message)


class InvalidPeriodicityException(Exception):
    """
    Exception raised when an invalid periodicity is provided.

    Attributes:
    -----------
    periodicity : str
        The invalid periodicity value provided.
    message : str
        A descriptive message indicating that the provided periodicity value is invalid.

    Methods:
    --------
    __init__(self, periodicity):
        Initializes the exception with the provided periodicity value and constructs the error message.
    """
    def __init__(self, periodicity):
        """
        Initializes the InvalidPeriodicityException with the provided periodicity value.

        Parameters:
        -----------
        periodicity : str
            The invalid periodicity value provided.
        """
        self.periodicity = periodicity
        self.message = f"Invalid periodicity: '{self.periodicity}'"
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """
    Exception raised when a user is not found.

    Attributes:
    -----------
    user_id : int
        The ID of the user that was not found.
    message : str
        A descriptive message indicating that the user with the specified ID was not found.

    Methods:
    --------
    __init__(self, user_id):
        Initializes the exception with the provided user ID and constructs the error message.
    """
    def __init__(self, user_id):
        """
        Initializes the UserNotFoundException with the provided user ID.

        Parameters:
        -----------
        user_id : int
            The ID of the user that was not found.
        """
        self.user_id = user_id
        self.message = f"User with ID {self.user_id} not found"
        super().__init__(self.message)


class UserAlreadyExistsException(Exception):
    """
    Exception raised when attempting to create a user that already exists.

    Attributes:
    -----------
    username : str
        The username of the user that already exists.
    message : str
        A descriptive message indicating that a user with the specified username already exists.

    Methods:
    --------
    __init__(self, username):
        Initializes the exception with the provided username and constructs the error message.
    """
    def __init__(self, username):
        """
        Initializes the UserAlreadyExistsException with the provided username.

        Parameters:
        -----------
        username : str
            The username of the user that already exists.
        """
        self.username = username
        self.message = f"User '{self.username}' already exists"
        super().__init__(self.message)


class UsernameAlreadyExistsException(Exception):
    """
    Exception raised when attempting to create a user with an existing username.

    Attributes:
    -----------
    username : str
        The username that already exists.
    message : str
        A descriptive message indicating that a user with the specified username already exists.

    Methods:
    --------
    __init__(self, username):
        Initializes the exception with the provided username and constructs the error message.
    """
    def __init__(self, username):
        """
        Initializes the UsernameAlreadyExistsException with the provided username.

        Parameters:
        -----------
        username : str
            The username that already exists.
        """
        self.username = username
        self.message = f"Username '{self.username}' already exists"
        super().__init__(self.message)
