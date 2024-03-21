import uuid
from datetime import datetime

class User:
    """
    A class to represent a user.

    Attributes:
    -----------
    username : str
        The name of the user.
    user_id : uuid.UUID
        The unique identifier for the user, defaults to a new UUID.
    created_at : str
        The date when the user was created, defaults to the current date in YYYY-MM-DD format.

    Methods:
    --------
    __init__(self, username, user_id=uuid.uuid4, created_at=str(datetime.now())[:10]):
        Initializes the User object with username, user_id, and created_at.
    get_user_id(self):
        Returns the unique identifier of the user.
    get_username(self):
        Returns the username of the user.
    get_created_at(self):
        Returns the creation date of the user account.
    set_username(self, username):
        Sets a new username for the user.
    __str__(self):
        Returns a string representation of the User object.
    """
    def __init__(self, username, user_id=uuid.uuid4(), created_at=str(datetime.now())[:10]):
        """
        Constructs all the necessary attributes for the User object.

        Parameters:
        -----------
        username : str
            The name of the user.
        user_id : uuid.UUID, optional
            The unique identifier for the user (default is a new UUID).
        created_at : str, optional
            The date when the user was created (default is the current date in YYYY-MM-DD format).
        """
        self.username = username
        self.user_id = user_id
        self.created_at = created_at

    def get_user_id(self):
        """
        Returns the unique identifier of the user.

        Returns:
        --------
        uuid.UUID
            The unique identifier of the user.
        """
        return self.user_id

    def get_username(self):
        """
        Returns the username of the user.

        Returns:
        --------
        str
            The username of the user.
        """
        return self.username
    
    def get_created_at(self):
        """
        Returns the creation date of the user account.

        Returns:
        --------
        str
            The creation date of the user account in YYYY-MM-DD format.
        """
        return self.created_at

    def set_username(self, username):
        """
        Sets a new username for the user.

        Parameters:
        -----------
        username : str
            The new username to be set for the user.
        """
        self.username = username

    def __str__(self):
        """
        Returns a string representation of the User object.

        Returns:
        --------
        str
            A string representation of the User object, including the user ID, username, and creation date.
        """
        return f"User ID: {self.user_id}\nUsername: {self.username}\nCreation Date: {self.created_at}"
