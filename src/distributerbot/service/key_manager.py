'''
Manages user keys, fresh keys, etc...
all key deliver and usage starts here.

also houses the management tools for
administrative use, ie
adding new keys, changing which roles can access
which keys, etc.

keys:
{
    
}

role_key_pairing:
{
    
}

user_redeemed_keys
{"<user_id>": 
    "used_keys": 
        {
            "key_itemization": {},
            "key_itemization": 
        }
}
using dictionary allows for O(1) search on whether or not
user has key, for example:

try:
    used_keys['1']['multiplayer_test']
    user has key
except:
    user doesn't have key yet
'''

from discord import User

class KeyObjectManager:
    '''
    This houses the functions for the key key itemizations
    '''
    def __init__(self):
        '''
        load from file & populate
        '''
        self.__key_definitions = {}

class UserKeyManager:
    '''
    This houses the functions for the 
    '''
    def __init__(self):
        return


class RoleKeyManager:
    def __init__(self):
        return


class KeyManager:
    '''
    This is the manager for the ENTIRE Key system
    '''
    def __init__(self):
        self.__key_object_manager = KeyObjectManager()
        self.__user_key_manager = UserKeyManager()
        self.__role_key_manager = RoleKeyManager()

    def give_key(self, user: User, key_type: str) -> str:
        return

    def remove_key(self, user: User, key_type: str) -> str:
        return
    