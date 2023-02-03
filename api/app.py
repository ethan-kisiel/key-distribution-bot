import discord
from os import environ
from json import load as load_json
from bot import bot
#CLIENT_SECRET = environ['CLIENT_SECRET']

authed_users = []
used_keys = {}

def initialization():

    '''
    Initializes all data structures that will
    be used at runtime for tracking user-key
    data, as well as authenticated users
    '''
    
    # load authed users
    try:
        with open('authed_users.txt') as txt_authed_users:
            authed_users = txt_authed_users.readlines()
            
    # create authed_users if it doesn't exist
    except FileNotFoundError:
        with open('authed_users.txt', 'w') as _:
            pass 
    
    # load used keys
    try:
        with open('used_keys.json') as json_used_keys:
            used_keys = load_json(json_used_keys)

    # create used_keys.json if it doesn't exist
    except FileNotFoundError:
        with open('used_keys.json', 'w') as _:
            pass
        
    # load key role pairing
    
def main():
    initialization()
    bot.run()


if __name__ == '__main__':
    main()