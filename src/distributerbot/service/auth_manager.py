import os

class AuthorityManager:
    '''
    handles user authority and user auth validation
    '''
    def __init__(self, auth_file: str):
        self.__authed_users = []
        
        path_to_auth_file = os.path.dirname(os.path.abspath(__file__))
        print(path_to_auth_file)
        path_to_auth_file += f'/{auth_file}'

        try:
            # attempt to initialize array of authorized users
            # from file
            with open(path_to_auth_file, 'r') as authed_users:
                self.__authed_users = authed_users.readlines()
                
        except FileNotFoundError:
            # create file if it doens't exist
            with open(path_to_auth_file, 'w') as _:
                pass

        except Exception as e:
            print(f'caught exception: {e}')

        finally:
            print('ERROR: Bad path')
            

    def has_auth(self, user_id: int):
        '''
        returns true if given user_id
        has authority
        '''
        return False
    
    def give_auth(self, user_id: int) -> bool:
        '''
        attempts to give authority
        to user id
        '''
        return False
        
    def remove_auth(self, user_id: int) -> bool:
        '''
        attempts to remove authority from
        given user id
        '''
        return False