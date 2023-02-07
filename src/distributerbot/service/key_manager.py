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
    key_type: 
    {
        display_name: "<Display Name>",
        description: "<optional description>"
    }
}

## available keys are the keys that this
## role is allowed to claim

role_key_pairing:
{
    role_name: "<discord role>",
    available_keys: ["key_name", "key_name"]
}

TODO: convert to use status values instead of True/False
for functions that don't specifically call for boolean return
value

'''
import json
from os import remove
from os.path import exists
from discord import User
from distributerbot.utils.database_manager import DatabaseManager

db_manager = DatabaseManager('user_keys')

class KeyObjectManager:
    '''
    This manages the key object definitions
    '''
    def __init__(self, keydef_file: str, keys_path: str):
        '''
        load from file & populate
        if json/key_objects.json does not exist,
        create it else, try set key definitions == to
        json
        keys_path is the location(name of folder),
        which you would like the key txt files to be stored.
        '''
        self.__key_definitions = {}
        self.__keydef_file = f'json/{keydef_file}.json'
        self.__keys_path = keys_path
        
        try:
            with open(self.__keydef_file, 'r') as json_key_objects:
                try:
                    self.__key_definitions = json.loads(json_key_objects)
                    
                except Exception as e:
                    print(f'Error while loading json: {e}')
                    
        except FileNotFoundError:
            # if it doesn't exist, initialize with the key defs dict
            self.sync_definitions()

        except Exception as e:
            print(f'Error: {e}')

    def set_key(self, key_type: str, display_name: str, description: str = ''):
        '''
        IN FUTURE, REFACTOR TO USE STATUS CODE
        adds new definition to key definitions
        returns True if successful
        False if not successful
        '''
        key = {'display_name': display_name, 'description': description}
        
        try:
            self.__key_definitions[key_type] = key
            
            # check if the keys path exists already if not, create it
            keys_path = f'{self.__keys_path}/{key_type}.txt'
            if not exists(keys_path):
                with open(keys_path, 'w') as _:
                    pass
    
        except:
            return False
        
        return self.sync_definitions()
    
    def remove_key(self, key_type: str):
        try:
            del self.__key_definitions[key_type]
            
            try:
                # try to remove keys file if it exists
                remove(f'{self.__keys_path}/{key_type}.txt')
            except:
                print(f'tried to remove nonexistent file: keys/{key_type}.txt')
        except:
            return False

        return self.sync_definitions()
    
    def key_exists(self, key_type: str):
        '''
        returns true if the given string is a key in
        key_definitions['keys'].keys()
        '''
        if key_type in self.get_key_types():
            return True

        return False
    
    def get_key_types(self):
        '''
        returns the strings of all available key types
        '''
        try:
            return self.__key_definitions.keys()
        except:
            print('Encountered an issue trying to fetch keys')
            return []

    def sync_definitions(self):
        '''
        attempts to save the current key definitions dict
        to json file
        Returns true if sync is successful else,
        returns false
        '''
        try:
            with open(self.__keydef_file, 'w') as json_file:
                json.dump(self.__key_definitions, json_file, indent=4)
            return True
        
        except:
            return False
        
    def clear_definitions(self):
        '''
        DEBUG DO NOT use in production
        '''
        for key in self.__key_definitions.keys():
            self.remove_key(key)

class RoleKeyManager:
    
    '''
    This controls which roles have
    access to which keys.
    
    pretty much the same as the key manager,
    but without the extra stuff for the key txt files
    '''
    def __init__(self, roledef_file: str):
        self.__role_keys = {'roles': {}}
        self.__roledef_file = f'json/{roledef_file}.json'
        
        try:
            with open(self.__roledef_file, 'r') as json_roles_objects:
                try:
                    self.__role_keys = json.loads(json_roles_objects)

                except Exception as e:
                    print(f'Error while loading json: {e}')
                    
        except FileNotFoundError:
            self.sync_role_keys()
    
        except Exception as e:
            print(f'Error: {e}')

    def add_role(self, role_name: str, role_keys=[]):
        # try to add a role
        # and sync
        self.__role_keys[role_name] = set(role_keys)
        return self.sync_role_keys()
    
    def remove_role(self, role_name: str):
        # if the role exists, remove it
        return
    
    def add_role_key(self, role_name: str, key_name: str):
        # check whether the role exists, if not, create role
        # add key to role
        return
    
    def remove_role_key(self, role_name: str, key_name: str):
        # check whether role exists if not exit with status 1
        # check if role contains the key if not exit with status 2
        # otherwise remove key from role and return 0 if sync == True
        return

    def get_roles():
        '''
        returns all role objects
        '''
        return

    def sync_role_keys(self):
        '''
        attempts to save the current key definitions dict
        to json file
        Returns true if sync is successful else,
        returns false
        '''
        try:
            with open(self.__roledef_file, 'w') as json_file:
                json.dump(self.__role_keys, json_file, indent=4)

            return True
        
        except:
            return False




class UserKeyManager:
    '''
    This talks with the database manager to find which
    keys the user has used.
    '''
    def __init__(self):
        return

class KeyManager(RoleKeyManager, UserKeyManager, KeyObjectManager):
    '''
    This is the manager for the ENTIRE Key system
    '''
    def __init__(self):
        return