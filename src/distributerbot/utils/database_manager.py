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
        
        
    async def get_user(self, user_id: int):
        with sessionmaker(self.engine)() as session:
            user = await (session.query(User)
                    .filter(User.user_id == user_id).first())

        return user

 
    async def create_user(self, user_id: int, name: str):
        '''
        Takes a user id integer, name string, attempts to create
        a user and return that user if successful
        '''
        user =  User(user_id, name)
        with sessionmaker(self.engine)() as session:
            session.add(user)

            try:
                await session.commit()
            except:
                print()
                return None

            return await session.query(User).get(user.user_id)


    async def give_key(self, user: User, key_def: dict,key: str):
        '''
        Takes a user, key def dictionary(from the key manager)
        Takes a key string, creates and returns a UsedKey database
        object.
        '''
        try:
            key = UsedKey(key, key_type=key_def['key_type'],
                          description=key_def['description'])
            key.owner = user
        except:
            return None

        with sessionmaker(self.engine)() as session:
            session.add(key)
            try:
                await session.commit()
            except:
                print('there was an issue saving the database')
                return None

        return key