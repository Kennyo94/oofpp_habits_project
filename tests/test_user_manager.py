import pytest 
from src.db_connection import DBConnection
from src.user_manager import UserManager
from src.models.habit import Habit
from src.models.user import User
from src.exceptions import UserAlreadyExistsException, UsernameAlreadyExistsException, UserNotFoundException
from datetime import datetime

user_1 = User("john_doe", 1, "2023-10-09")
user_2 = User("jane_doe", 2, "2024-01-09")
user_3 = User("max_mustermann", 3, "2024-03-15")


@pytest.fixture(scope="class")
def db_manager():
    manager = DBConnection("../db/test_database.db")
    manager.create_tables()
    u_manager = UserManager(manager)

    u_manager.import_user(user_1)
    u_manager.import_user(user_2)
    u_manager.import_user(user_3)

    yield manager
    manager.delete_tables()



class TestUserManager:

    def test_get_users(self, db_manager):
        user_manager = UserManager(db_manager)
        users = user_manager.get_users()
        assert len(users) == 3

    def test_get_user_by_id(self, db_manager):
        user_manager = UserManager(db_manager)
        user = user_manager.get_user_by_id(1)
        assert user_1.get_user_id() == user.get_user_id()
        assert user_1.get_username() == user.get_username()

    def test_get_user_by_name(self, db_manager):
        user_manager = UserManager(db_manager)
        user = user_manager.get_user_by_name("john_doe")
        assert user_1.get_user_id() == user.get_user_id()
        assert user_1.get_username() == user.get_username()

    def test_get_user_not_found_by_id(self, db_manager):
        user_manager = UserManager(db_manager)
        with pytest.raises(UserNotFoundException):
            user = user_manager.get_user_by_id(200)

    def test_get_user_not_found_by_name(self, db_manager):
        user_manager = UserManager(db_manager)
        with pytest.raises(UserNotFoundException):
            user = user_manager.get_user_by_name("TestNameNotFound")

    def test_create_user(self, db_manager):
        user_manager = UserManager(db_manager)
        user_manager.create_user("TestNameUser")
        user = user_manager.get_user_by_name("TestNameUser")
        assert user is not None
        assert user.get_username() == "TestNameUser"
        assert user.get_user_id() == 4

    def test_create_user_username_exists(self, db_manager):
        user_manager = UserManager(db_manager)
        with pytest.raises(UsernameAlreadyExistsException):
            user_manager.create_user("john_doe")


    def test_import_user(self, db_manager):
        user_manager = UserManager(db_manager)
        user_manager.import_user(User("TestUser"))
        user = user_manager.get_user_by_name("TestUser")
        assert user is not None
        assert user.get_user_id() == 5
        assert user.get_username() == "TestUser"
    
    def test_import_user_already_exists(self, db_manager):
        user_manager = UserManager(db_manager)
        with pytest.raises(UserAlreadyExistsException):
            user_manager.import_user(User("john_doe"))


    def test_delete_user_by_username(self, db_manager):
        user_manager = UserManager(db_manager)
        user_manager.delete_user_by_username("john_doe")
        with pytest.raises(UserNotFoundException):
            user_manager.get_user_by_name("john_doe")

    
    def test_delete_user_by_id(self, db_manager):
        user_manager = UserManager(db_manager)
        user_manager.delete_user_by_id(2)
        with pytest.raises(UserNotFoundException):
            user_manager.get_user_by_id(2)





    