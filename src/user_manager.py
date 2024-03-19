from models.user import User
from db_connection import DBConnection
from datetime import datetime 
from exceptions import UserNotFoundException, UsernameAlreadyExistsException, UserAlreadyExistsException


class UserManager:

    def __init__(self, db_connection):
        self.db = db_connection

    def get_users(self):
        query = "SELECT * FROM Users"
        result = self.db.execute_query(query).fetchall()
        if result is not None:
            return [User(user[1], user[0], user[2]) for user in result]
        else: 
            return []

    def get_user_by_name(self, username):
        query = "SELECT * FROM Users WHERE username = ?"
        result = self.db.execute_query(query, (username, )).fetchone()
        if result is not None:
            return User(result[1], result[0], result[2])
        else:
            raise UserNotFoundException("-")

    
    def get_user_by_id(self, user_id):
        query = "SELECT * FROM Users WHERE user_id = ?"
        result = self.db.execute_query(query, (user_id, )).fetchone()
        if result is not None:
            return User(result[1], result[0], result[2])
        else:
            raise UserNotFoundException(user_id)
    
    

    def create_user(self, username):
        query_check = "SELECT * FROM Users WHERE username = ?"
        user_to_be_added = self.db.execute_query(query_check, (username, )).fetchone()      
        if user_to_be_added is None:
            query = "INSERT INTO Users (username, created_at) VALUES (?, ?)"
            self.db.execute_query(query, (username, str(datetime.now())[:10])) 
            self.db.commit_query()
        else:
            raise UsernameAlreadyExistsException(username)
        
    def import_user(self, user):
        query_check = "SELECT * FROM Users WHERE username = ?"
        user_to_be_added = self.db.execute_query(query_check, (user.get_username(), )).fetchone() 
        if user_to_be_added is None:
            query = "INSERT INTO Users (username, created_at) VALUES (?, ?)"
            self.db.execute_query(query, (user.get_username(), user.get_created_at())) 
            self.db.commit_query()
        else:
            raise UserAlreadyExistsException(user.get_username())
    
    def delete_user_by_username(self, username):
        query_check = "SELECT * FROM Users WHERE username = ?"
        user_to_be_deleted = self.db.execute_query(query_check, (username, )).fetchone()      
        if user_to_be_deleted is not None:
            query = "DELETE FROM Users WHERE username = ?"
            self.db.execute_query(query, (username,)) 
            self.db.commit_query()
            return "SUCCESS"
        else:
            print(user_to_be_deleted)
            raise UserNotFoundException(user_to_be_deleted[0])

    def delete_user_by_id(self, user_id):
        query_check = "SELECT * FROM Users WHERE user_id = ?"
        user_to_be_deleted = self.db.execute_query(query_check, (user_id, )).fetchone()      
        if user_to_be_deleted is not None:
            query = "DELETE FROM Users WHERE user_id = ?"
            self.db.execute_query(query, (user_id,)) 
            self.db.commit_query()
            return "SUCCESS"
        else:
            print(user_to_be_deleted)
            raise UserNotFoundException(user_id)
        

    

    

    

        


