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
        
    def create_key(self, key_type: str, display_name: str, description: str = ''):
        '''
        adds new definition to key definitions
        '''
        return
    
    def remove_key(self, key_type: str):
        return

    # MARK: Make this async
    # MARK: Possibly run on seperate thread if client wishes
    def sync_definitions(self):
        # ONLY USE IN DEBUG
        return

class UserKeyManager:
    '''
    This houses the functionality for which keys each user has claimed
    '''
    def __init__(self):
        self.__used_keys = {}
        
    def sync_used_keys(self):
        return


class RoleKeyManager:
    '''
    This houses the functions for
    '''
    def __init__(self):
        self.__role_keys = {}
        
    def add_role(self, role_name: str):
        return
    
    def remove_role(self, role_name: str):
        return
    
    def add_role_key(self, role_name: str, key_name: str):
        return

    def sync_role_keys(self):
        return

class KeyManager(RoleKeyManager, UserKeyManager, KeyObjectManager):
    '''
    This is the manager for the ENTIRE Key system
    '''
    def __init__(self):
        pass

    def give_key(self, user: User, key_type: str) -> str:
        return

    def remove_player_key(self, user: User, key_type: str) -> str:
        '''
        DANGER Keys should (almost never) be removed from player
        '''
        return