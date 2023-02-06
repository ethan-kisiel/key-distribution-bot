from distributerbot.utils.database_manager import DatabaseManager
from distributerbot.models.base_models import User
from sqlalchemy.orm import sessionmaker


db_manager = DatabaseManager('TEST_DB')

def test_db_manager_init():
    Session = sessionmaker(bind=db_manager.engine)
    
    new_user = User(name='Ethan', user_id=8080)
    
    session = Session()
    
    ethan = None

    session.add(new_user)
    session.commit()
    session.close()
    
    session = Session()
    
    ethan = session.query(User).filter(User.name == 'Ethan').first()
    
    assert(ethan != None)
    
    