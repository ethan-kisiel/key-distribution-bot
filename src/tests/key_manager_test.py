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