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
from discord import User, Member
from distributerbot.utils.database_manager import DatabaseManager

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
                    contents = json_key_objects.read()
                    
                    self.__key_definitions = json.loads(contents)
                    
                except Exception as e:
                    print(f'Error while loading json: {e}')
                    
        except FileNotFoundError:
            # if it doesn't exist, initialize with the key defs dict
            self.sync_definitions()

        except Exception as e:
            print(f'Error: {e}')

    def get_key_data(self, key_type: str):
        try:
            return self.__key_definitions[key_type]
        except:
            return None

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
    
        except Exception as e:
            print(f'exception raised: {e}')
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
        return key_type in self.get_key_types()
    
    def get_key_types(self):
        '''
        returns the strings of all available key types
        '''
        return self.__key_definitions.keys()
    
    def retrieve_key(self, key_type: str):
        key = ''
        try:
            with open(f'{self.__keys_path}/{key_type}.txt', 'r') as key_file:
                file_lines = key_file.readlines()
                # write all lines, excluding the first (0th) line
                key = file_lines[0].strip('\n').strip()
                
            with open(f'{self.__keys_path}/{key_type}.txt', 'w') as key_file:
                key_file.writelines(file_lines[1:])

            return key

        except:
            print('Error while retrieving key from file')

        return None

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
        self.__role_keys = {}
        self.__roledef_file = f'json/{roledef_file}.json'
        
        try:
            with open(self.__roledef_file, 'r') as json_roles_objects:
                try:
                    contents = json_roles_objects.read()
                    
                    self.__role_keys = json.loads(contents)

                except Exception as e:
                    print(f'Error while loading json: {e}')
                    
        except FileNotFoundError:
            self.sync_role_keys()
    
        except Exception as e:
            print(f'Error: {e}')

    
    def set_role(self, role_name: str, role_keys=[]):
        try:
            self.__role_keys[role_name] = role_keys
        except:
            print(f'error trying to convert role_keys to set')
            return False

        return self.sync_role_keys()
    
    def remove_role(self, role_name: str):
        try:
            del self.__role_keys[role_name]
        except:
            print('Failure trying to delete role')
            return False
        
        return self.sync_role_keys()

    def add_role_key(self, role_name: str, key_type: str):
        '''
        check whether the role exists, if not, create role
        add key to role
        '''
        try:
            if self.role_exists(role_name):
                self.__role_keys[role_name].append(key_type)
                return self.sync_role_keys()
            else:
                self.add_role(role_name)
                return self.add_role_key(role_name, key_type)
        except:
            print('Something went wrong')
            return False
    
    def remove_role_key(self, role_name: str, key_type: str):
        '''
        Removes key from role and returns 0 if key is present in
        role, returns 1 if role doesn't exist,
        returns 2 if key isn't present in role
        '''
        if not self.role_exists(role_name):
            return 1

        if key_type in self.__role_keys[role_name]:
            self.__role_keys[role_name].remove(key_type)
            self.sync_role_keys()
            
            return 0

        return 2

    def get_roles(self):
        return list(self.__role_keys.keys())

    def get_role_keys(self, role_name: str):
        if self.role_exists(role_name):
            return self.__role_keys[role_name]
        
        return []

    def role_exists(self, role_name: str):
        return role_name in self.get_roles()

    def role_contains_key(self, role_name: str, key_type: str):
        try:
            return key_type in self.__role_keys[role_name]
        except:
            return False

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
            print('ERROR while syncing role keys!')
            return False

    def clear_role_keys(self):
        self.__role_keys = {}
        


class KeyManager(RoleKeyManager, KeyObjectManager):
    '''
    This is the manager for the ENTIRE Key system
    '''
    def __init__(self, roledef_file: str, keydef_file: str, keys_folder: str, db_name: str):
        RoleKeyManager.__init__(self, roledef_file)
        KeyObjectManager.__init__(self, keydef_file, keys_folder)
        self.db_manager = DatabaseManager(db_name)

    def get_user_available_keys(self, member: Member):
        key_roles = self.get_roles()
        user_roles = [role.name for role in member.roles if role.name in key_roles]
        
        for role in user_roles:
            if role in key_roles:
                return self.get_role_keys(role)

    def give_user_keys(self, user: User, keys=[]):
        '''
        tries to give user a list of keys
        will give user keys if user doesn't already
        have them.
        '''
        db_user =  self.db_manager.get_user(user.id)
        
        if db_user is None:
            self.db_manager.create_user(user.id, user.name)
            db_user = self.db_manager.get_user(user.id)

        user_keys = self.db_manager.get_user_keys(user.id)
        if len(user_keys) > 0:
            # limit user keys to just a list of key.key_type
            user_keys = [key.key_type for key in user_keys]
            print(user_keys)
            # limit keys to only those which aren't in user_keys
            keys = [key for key in keys if key not in user_keys]
            
        print(keys)
        for key in keys:
            key_code = self.retrieve_key(key)
            if key_code:
                key_data = self.get_key_data(key)
                oid = db_user.id
                self.db_manager.give_key(oid, key_code, key, key_data)

        
        # step 1 limit the keys we try to create to just the ones
        # that the user doesn't already have
        # step 2 try to create a key with data from key obj man
        # step 3 give the user the key
        

    
    def delete_key(self, key_type: str):
        '''
        this function coordinates between the KeyObjectManager
        and the RoleKeyManager, to make sure that the
        RoleKeyManager doesn't contain nonexistent keys.
        '''
        try:
            for role in self.get_roles():
                if self.role_contains_key(role, key_type):
                    self.remove_role_key(role, key_type)

            return self.remove_key(key_type)
        except:
            return False
        
    def set_role_keys(self, role_name: str, keys=[]):
        '''
        this performs set role using only valid keys.
        basically just validation.
        '''
        
        valid_keys = [key for key in keys if self.key_exists(key)]
        
        return self.set_role(role_name, valid_keys)
