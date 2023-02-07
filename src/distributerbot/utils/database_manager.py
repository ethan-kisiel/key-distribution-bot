'''
bindings for the database sql queries
'''
from distributerbot.models.base_models import User, UsedKey, Base
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    '''
    This class handles all interaction with the database.
    '''
    def __init__(self, db_name: str):
        try:
            self.engine = create_engine(f'sqlite:///{db_name}.db')
        except Exception as e: 
            print('an error occurred while instantiating database')

        Base.metadata.create_all(self.engine)
        
        
    def get_user(self, user_id: int):
        with sessionmaker(self.engine)() as session:
            user = (session.query(User)
                    .filter(User.user_id == user_id).first())

        return user

    def get_user_keys(self, user_id: int):
        with sessionmaker(self.engine)() as session:
            user = (session.query(User)
                    .filter(User.user_id == user_id).first())
            
            try:
                return user.used_keys
            except Exception as e:
                print(f'EXCEPTION RAISED: {e}')
            
            return []

    def create_user(self, user_id: int, name: str):
        '''
        Takes a user id integer, name string, attempts to create
        a user, returns status code 0 = success; 1 = failure creating
        user, 2 = failure persisting user
        '''
        try:
            user =  User(user_id, name)
        except:
            return 1

        with sessionmaker(self.engine)() as session:
            try:
                session.add(user)
                session.commit()
            except Exception as e:
                print(f'error: {e}')
                return 2

            return 0


    def give_key(self, owner_id: str, key_def: dict,key: str):
        '''
        Takes a user, key def dictionary(from the key manager)
        Takes a key string, creates and returns a status code
        0 = success; 1 = failure creating key; 2 = failure
        persisting key
        '''
        try:
            key = UsedKey(key, key_type=key_def['key_type'],
                          description=key_def['description'])
            
        except Exception as e:
            print(f'RAISED EXCEPTION: {e}')
            return 1

        with sessionmaker(self.engine)() as session:
            key.owner = session.query(User).get(owner_id)
            try:
                session.add(key)
                session.commit()
            except:
                print('there was an issue saving the database')
                return 2

            return 0
        
        
    def clear(self):
        '''
        DANGER DO NOT FOR ANY REASON hook this up
        DEBUG ONLY!!!!
        '''
        with sessionmaker(self.engine)(autoflush=True) as session:
            session.query(User).delete()

            session.commit()