import uuid
from datetime import datetime

class User:

    def __init__(self, username, user_id=uuid.uuid4, created_at=str(datetime.now())[:10]):

        self.username = username
        self.user_id = user_id
        self.created_at = created_at

    def get_user_id(self):
        return self.user_id

    def get_username(self):
        return self.username
    
    def get_created_at(self):
        return self.created_at

    def set_username(self, username):
        self.username = username
    

    def __str__(self):
        return f"User ID: {self.user_id}\nUsername: {self.username}\nCreation Date: {self.created_at}"

