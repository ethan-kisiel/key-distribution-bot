import discord

from os import environ
from distributerbot.api.bot import bot
from distributerbot.service.auth_manager import AuthorityManager
from json import load as load_json

# import environment variables
import environment_vars
CLIENT_SECRET = environ['CLIENT_SECRET']

auth_manager = AuthorityManager(auth_file='AUTHED_USERS.txt')

def main():
    bot.run(CLIENT_SECRET)


if __name__ == '__main__':
    main()