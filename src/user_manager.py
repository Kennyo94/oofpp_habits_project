from src.models.user import User
from src.db_connection import DBConnection
from datetime import datetime
from src.exceptions import UserNotFoundException, UsernameAlreadyExistsException, UserAlreadyExistsException


class UserManager:
    """
    A class to manage user-related operations.

    Attributes:
    -----------
    db : DBConnection
        An instance of the database connection.

    Methods:
    --------
    get_users(self) -> list[User]:
        Retrieves all users from the database.

    get_user_by_name(self, username) -> User:
        Retrieves a user by their username from the database.

    get_user_by_id(self, user_id) -> User:
        Retrieves a user by their ID from the database.

    create_user(self, username):
        Creates a new user in the database with the given username.

    import_user(self, user: User):
        Imports an existing user object into the database.

    delete_user_by_username(self, username):
        Deletes a user from the database by their username.

    delete_user_by_id(self, user_id):
        Deletes a user from the database by their ID.
    """
    def __init__(self, db_connection):
        """
        Initializes the UserManager with the provided database connection.

        Parameters:
        -----------
        db_connection : DBConnection
            An instance of the database connection.
        """
        self.db = db_connection

    def get_users(self) -> list:
        """
        Retrieves all users from the database.

        Returns:
        --------
        list[User]:
            A list of User objects representing all users in the database.
        """
        query = "SELECT * FROM Users"
        result = self.db.execute_query(query).fetchall()
        if result is not None:
            return [User(user[1], user[0], user[2]) for user in result]
        else:
            return []

    def get_user_by_name(self, username) -> User:
        """
        Retrieves a user by their username from the database.

        Parameters:
        -----------
        username : str
            The username of the user to retrieve.

        Returns:
        --------
        User:
            A User object representing the retrieved user.

        Raises:
        -------
        UserNotFoundException:
            If no user with the specified username is found in the database.
        """
        query = "SELECT * FROM Users WHERE username = ?"
        result = self.db.execute_query(query, (username,)).fetchone()
        if result is not None:
            return User(result[1], result[0], result[2])
        else:
            raise UserNotFoundException("-")

    def get_user_by_id(self, user_id) -> User:
        """
        Retrieves a user by their ID from the database.

        Parameters:
        -----------
        user_id : int
            The ID of the user to retrieve.

        Returns:
        --------
        User:
            A User object representing the retrieved user.

        Raises:
        -------
        UserNotFoundException:
            If no user with the specified ID is found in the database.
        """
        query = "SELECT * FROM Users WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id,)).fetchone()
        if result is not None:
            return User(result[1], result[0], result[2])
        else:
            raise UserNotFoundException(user_id)

    def create_user(self, username):
        """
        Creates a new user in the database with the given username.

        Parameters:
        -----------
        username : str
            The username of the user to create.

        Raises:
        -------
        UsernameAlreadyExistsException:
            If a user with the specified username already exists in the database.
        """
        query_check = "SELECT * FROM Users WHERE username = ?"
        user_to_be_added = self.db.execute_query(query_check, (username,)).fetchone()
        if user_to_be_added is None:
            query = "INSERT INTO Users (username, created_at) VALUES (?, ?)"
            self.db.execute_query(query, (username, str(datetime.now())[:10]))
            self.db.commit_query()
        else:
            raise UsernameAlreadyExistsException(username)

    def import_user(self, user: User):
        """
        Imports an existing user object into the database.

        Parameters:
        -----------
        user : User
            The User object to import into the database.

        Raises:
        -------
        UserAlreadyExistsException:
            If a user with the same username already exists in the database.
        """
        query_check = "SELECT * FROM Users WHERE username = ?"
        user_to_be_added = self.db.execute_query(query_check, (user.get_username(),)).fetchone()
        if user_to_be_added is None:
            query = "INSERT INTO Users (username, created_at) VALUES (?, ?)"
            self.db.execute_query(query, (user.get_username(), user.get_created_at()))
            self.db.commit_query()
        else:
            raise UserAlreadyExistsException(user.get_username())

    
    def delete_user_by_username(self, username):
        """
        Deletes a user from the database by their username.

        Parameters:
        -----------
        username : str
            The username of the user to be deleted.

        Returns:
        --------
        str
            A success message indicating the deletion was successful.

        Raises:
        -------
        UserNotFoundException
            If no user with the given username is found in the database.
        """
        query_check = "SELECT * FROM Users WHERE username = ?"
        user_to_be_deleted = self.db.execute_query(query_check, (username, )).fetchone()
        if user_to_be_deleted is not None:
            query = "DELETE FROM Users WHERE username = ?"
            self.db.execute_query(query, (username,))
            self.db.commit_query()
            return "SUCCESS"
        else:
            raise UserNotFoundException(username)
        

    def delete_user_by_id(self, user_id):
        """
        Deletes a user from the database by their user ID.

        Parameters:
        -----------
        user_id : int
            The ID of the user to be deleted.

        Returns:
        --------
        str
            A success message indicating the deletion was successful.

        Raises:
        -------
        UserNotFoundException
            If no user with the given ID is found in the database.
        """
        query_check = "SELECT * FROM Users WHERE user_id = ?"
        user_to_be_deleted = self.db.execute_query(query_check, (user_id,)).fetchone()
        if user_to_be_deleted is not None:
            query = "DELETE FROM Users WHERE user_id = ?"
            self.db.execute_query(query, (user_id,))
            self.db.commit_query()
            return "SUCCESS"
        else:
            raise UserNotFoundException(user_id)

    

    

        


