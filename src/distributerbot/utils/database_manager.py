'''
bindings for the database sql queries
'''
from distributerbot.models.base_models import User, UsedKey, Base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    
    def __init__(self, db_name: str):
        try:
            self.engine = create_engine(f'sqlite:///{db_name}.db')
        except Exception as e: 
            print("an error occurred while instantiating database")

        Base.metadata.create_all(self.engine)
        
    def get_user(self, user_id: int):
        return
    
    def create_user(self):
        return
    
    def get_user_keys(self, user_id):
        return
    
    def create_key(self):
        return

