import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship



Base = declarative_base()

class UsedKey(Base):

    __tablename__ = 'used_keys'
    
    # key_value is the actual key.. should probably be encrypted
    key_value = Column("key_value", String, primary_key=True)
    key_type = Column("key_type", String)
    key_description = Column("key_description", String)
    key_name = Column("key_name", String)
    date_used = Column("date_used", String)
    
    user_id = Column(Integer, ForeignKey("user.user_id"))
    used_by = relationship("User", back_populates="used_keys")
   
    
    def __init__(self, key_value: str, key_type: str):
        self.key_value = key_value
        self.key_type = key_type

    def __repr__(self) -> str:
        return f"key_type={self.key_type}, key_value={self.key_value}"
    

class User(Base):

    __tablename__ = "users"
    
    # user_id == discord uuid
    user_id = Column("user_id", Integer, primary_key=True)
    used_keys = relationship("UsedKey")
    
    def __init__(self, user_id: int, user_name: str):
        self.user_id = user_id
        self.user_name = user_name
    
    def __repr__(self) -> str:
        return f"user_id={self.user_id}, used_keys={len(self.used_keys)}"