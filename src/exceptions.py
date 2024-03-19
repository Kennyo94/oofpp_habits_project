

class HabitNotFoundException(Exception):
    """Exception raised when a habit is not found."""

    def __init__(self, habit_id):
        self.habit_id = habit_id
        self.message = f"Habit with ID {self.habit_id} not found"
        super().__init__(self.message)


class HabitAlreadyExistsException(Exception):
    """Exception raised when attempting to create a habit that already exists."""

    def __init__(self, habit_name):
        self.habit_name = habit_name
        self.message = f"Habit '{self.habit_name}' already exists"
        super().__init__(self.message)


class InvalidPeriodicityException(Exception):
    """Exception raised when an invalid periodicity is provided."""

    def __init__(self, periodicity):
        self.periodicity = periodicity
        self.message = f"Invalid periodicity: '{self.periodicity}'"
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """Exception raised when a user is not found."""

    def __init__(self, user_id):
        self.user_id = user_id
        self.message = f"User with ID {self.user_id} not found"
        super().__init__(self.message)

class UserAlreadyExistsException(Exception):
    """Exception raised when attempting to create a user that already exists."""

    def __init__(self, username):
        self.username = username
        self.message = f"User '{self.username}' already exists"
        super().__init__(self.message)


class UsernameAlreadyExistsException(Exception):
    """Exception raised when attempting to create a user with an existing username."""

    def __init__(self, username):
        self.username = username
        self.message = f"Username '{self.username}' already exists"
        super().__init__(self.message)
