from distributerbot.service.key_manager import *

import os
import json
import pytest

class TestKeyObjectManager:
    @pytest.fixture
    def key_object_manager(self):
        return KeyObjectManager('key_objects', 'keys')
        
    def test_create_key(self, key_object_manager):
        assert key_object_manager.set_key('test_key', 'Test Key', 'This is a test key')
        assert 'test_key' in key_object_manager.get_key_types()
        assert os.path.exists('keys/test_key.txt')
        
    def test_remove_key(self, key_object_manager):
        key_object_manager.set_key('test_key', 'Test Key', 'This is a test key')
        assert key_object_manager.remove_key('test_key')
        assert 'test_key' not in key_object_manager.get_key_types()
        assert not os.path.exists('keys/test_key.txt')

        key_object_manager.clear_definitions()
        

    def test_key_exists(self, key_object_manager):
        key_object_manager.set_key('test_key', 'Test Key', 'This is a test key')
        assert key_object_manager.key_exists('test_key')
        assert not key_object_manager.key_exists('nonexistent_key')
        
    def test_get_key_types(self, key_object_manager):
        key_object_manager.set_key('test_key', 'Test Key', 'This is a test key')
        key_types = key_object_manager.get_key_types()
        assert 'test_key' in key_types



class TestRoleKeyManager:
    @pytest.fixture
    def rkm(self):
        return RoleKeyManager('roledef.json')
    
    def test_add_role(self, rkm):
        rkm.clear_role_keys()
        assert rkm.add_role("admin", ["key1", "key2"]) == True
        assert "admin" in rkm.get_roles()

    def test_remove_role(self, rkm):
        rkm.clear_role_keys()
        rkm.add_role("admin", ["key1", "key2"])
        assert rkm.remove_role("admin") == True
        assert "admin" not in rkm.get_roles()
        
    def test_add_role_key(self, rkm):
        rkm.clear_role_keys()
        rkm.add_role("admin", ["key1", "key2"])
        assert rkm.add_role_key("admin", "key3") == True
        assert rkm.get_role_keys("admin") == ["key1", "key2", "key3"]
        
    def test_remove_role_key(self, rkm):
        rkm.clear_role_keys()
        rkm.add_role("admin", ["key1", "key2"])
        assert rkm.remove_role_key("admin", "key1") == 0
        assert rkm.get_role_keys("admin") == ["key2"]
        
    def test_get_roles(self, rkm):
        rkm.clear_role_keys()
        rkm.add_role("admin", ["key1", "key2"])
        rkm.add_role("user", ["key3", "key4"])
        assert rkm.get_roles() == ["admin", "user"]
        
    def test_role_exists(self, rkm):
        rkm.clear_role_keys()
        rkm.add_role("admin", ["key1", "key2"])
        assert rkm.role_exists("admin") == True
        assert rkm.role_exists("user") == False