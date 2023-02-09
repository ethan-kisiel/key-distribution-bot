from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from uuid import uuid4
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True)

    user_id = Column(Integer)
    name = Column(String)

    used_keys = relationship("UsedKey", back_populates="owner",
                             cascade="all, delete-orphan")
    
    def __init__(self, user_id: int, name: str):
        self.id = str(uuid4())
        
        self.user_id = user_id
        self.name = name
    
    def __repr__(self):
        return f'user_id={self.user_id}, name={self.name}'

class UsedKey(Base):
    __tablename__ = 'used_keys'

    id = Column(String, primary_key=True)
    
    key_type = Column(String)
    key = Column(String)
    display_name = Column(String)
    description = Column(String)
    
    used_date = Column(String)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="used_keys")
    
    def __init__(self, key: str, key_type: str, display_name: str, description: str=''):
        self.id = str(uuid4())

        self.used_date = (datetime.now()
                          .strftime("%H:%M:%S-%m/%d/%Y"))

        self.key = key
        self.key_type = key_type
        self.display_name = display_name
        self.description = description

    def __repr__(self):
        return f'owner={self.owner_id}, used_date={self.used_date}'