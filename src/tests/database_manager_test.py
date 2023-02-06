import pytest
from distributerbot.models.base_models import User, UsedKey
from distributerbot.utils.database_manager import DatabaseManager

@pytest.fixture
def db_manager():
    return DatabaseManager('test_db')

def test_create_user(db_manager):
    db_manager.clear()
    status = db_manager.create_user(1, "test_user")
    assert status == 0
    user = db_manager.get_user(1)
    assert user.user_id == 1
    assert user.name == "test_user"

def test_give_key(db_manager):
    db_manager.clear()
    db_manager.create_user(1, "test_user")
    user = db_manager.get_user(1)
    key_def = {
        "key_type": "test_key",
        "description": "test_description"
    }
    status = db_manager.give_key(user.id, key_def, "test_key")
    assert status == 0

    keys = db_manager.get_user_keys(1)
    
    assert len(keys) == 1
    key = keys[0]
    assert key.key == "test_key"
    assert key.key_type == "test_key"
    assert key.description == "test_description"