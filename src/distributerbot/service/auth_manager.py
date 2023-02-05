import os

class AuthorityManager:
    '''
    handles user authority and user auth validation
    '''
    def __init__(self, auth_file: str):
        '''
        takes string auth_file which is the name
        that you wish to have before the .txt extension
        DO NOT add .txt when initializing this object
        '''
        self.__authed_users = []
        
        # get the file path to this directory
        abs_path = os.path.abspath(__file__)
        path_to_auth_file = os.path.dirname(abs_path)
        path_to_auth_file += f'/{auth_file}.txt'
        
        self.__file_path = path_to_auth_file
        
        try:
            # attempt to initialize array of authorized users
            # from file
            with open(self.__file_path, 'r') as authed_users:
                self.__authed_users = [line.strip('\n') for line in authed_users.readlines()]
                
                for line in self.__authed_users:
                    print(line)
                
        except FileNotFoundError:
            # create file if it doens't exist
            with open(self.__file_path, 'w') as _:
                pass

        except Exception as e:
            print(f'ERROR: {e}')
            
    # member functions
    def has_auth(self, user_id: int):
        '''
        returns true if given user_id
        has authority
        '''
        if str(user_id) in self.__authed_users:
            return True

        return False

    def give_auth(self, user_id: int) -> bool:
        '''
        attempts to give authority
        to user id
        '''
        if not self.has_auth(user_id):
            self.__authed_users.append(str(user_id))
            return self.sync_auth_file()

        return False
        
    def remove_auth(self, user_id: int) -> bool:
        '''
        attempts to remove authority from
        given user id
        '''
        if self.has_auth(user_id=user_id):
            self.__authed_users.remove(str(user_id))
            return self.sync_auth_file()

        return False
    
    def sync_auth_file(self):
        '''
        This will overwrite the auth file with the
        current contents of authed_users
        '''
        try:
            with open(self.__file_path, 'w') as auth_file:
                for item in self.__authed_users:
                    auth_file.write(f'{item}\n')
            return True

        except:
            print('Failed to sync')
            return False
        

    def clear_auth(self) -> bool:
        '''
        DANGER this will remove all authentication contents
        only use for debug purposes
        '''
        self.__authed_users = []
        try:
            with open(self.__file_path, 'w') as _:
                pass
            return True

        except:
            return False
    
    def remove_auth_file(self) -> bool:
        '''
        DANGER this will ENTIRELY REMOVE auth file
        for test cleanup only
        '''
        try:
            os.remove(self.__file_path)
            return True

        except:
            return False
        
    def __repr__(self):
        return f'filepath={self.__file_path}'
    
