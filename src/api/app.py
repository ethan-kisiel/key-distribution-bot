import discord

from os import environ
from bot import bot

from json import load as load_json
from sys import path as syspath

syspath.append('../src/')
import environment_vars

CLIENT_SECRET = environ['CLIENT_SECRET']


authed_users = []
used_keys = {}
role_key_pairing = {}


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
    finally:
        print('bad error')
    
    # load used keys
    try:
        with open('keys/used_keys.json') as json_used_keys:
            try:
                used_keys = load_json(json_used_keys)
            except Exception as e:
                print(e)

    # create used_keys.json if it doesn't exist
    except FileNotFoundError:
        with open('keys/used_keys.json', 'w') as _:
            pass
    finally:
        print('bad error')
        
    # load key role pairing
    
def main():
    initialization()
    bot.run(CLIENT_SECRET)


if __name__ == '__main__':
    main()