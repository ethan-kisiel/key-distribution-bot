from distributerbot.utils.database_manager import DatabaseManager
from distributerbot.models.base_models import User
from sqlalchemy.orm import sessionmaker


db_manager = DatabaseManager('TEST_DB')

def test_db_manager_add_user():
    ## USE db_manager.create_user()
    
    ## Create session maker and query for created user
    return

def test_db_manager_add_key():
    ## CREATE user with Session maker
    ## USE db_manager.add_key()
    return

def test_db_manager_get_user():
    ## CREATE user with session maker
    ## use db_manager.get_user() to get that user
    return
    