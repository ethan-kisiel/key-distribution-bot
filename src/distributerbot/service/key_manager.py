'''
Manages user keys, fresh keys, etc...
all key deliver and usage starts here.

also houses the management tools for
administrative use, ie
adding new keys, changing which roles can access
which keys, etc.

## key type is used for the back end
## should be lowercased, no spaces
## this also becomes the txt file,
## which will house the raw keys
keys:
{
    key_type: "<key_type>",
    display_name: "<Display Name>",
    description: "<optional description>"
}

## available keys are the keys that this
## role is allowed to claim

role_key_pairing:
{
    role_name: "<discord role>",
    available_keys: ["key_name", "key_name"]
}

'''
import json
from discord import User
from distributerbot.utils.database_manager import DatabaseManager

db_manager = DatabaseManager()

class KeyObjectManager:
    '''
    This manages the key object definitions
    '''
    def __init__(self):
        '''
        load from file & populate
        if json/key_objects.json does not exist,
        create it else, try set key definitions == to
        json
        '''
        self.__key_definitions = {}
        
        try:
            with open('json/key_objects.json', 'r') as json_key_objects:
                try:
                    self.__key_definitions = json.loads(json_key_objects)
                    
                except Exception as e:
                    print(f'Error while loading json: {e}')
                    
        except FileNotFoundError:
            # create file
            with open('json/key_objects.json', 'r'):
                pass

        except Exception as e:
            print('Error: {e}')
        


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
    This talks with the database manager to find which
    keys the user has used.
    '''
    def __init__(self):
        return



class RoleKeyManager:
    '''
    This controls which roles have
    access to which keys.
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
        return

    def give_key(self, user: User, key_type: str) -> str:
        # call db and remove key from text file
        return

    def remove_player_key(self, user: User, key_type: str) -> str:
        '''
        DANGER Keys should (almost never) be removed from player
        '''
        return