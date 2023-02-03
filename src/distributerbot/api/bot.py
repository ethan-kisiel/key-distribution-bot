import asyncio
import discord
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.message_content = True

bot = Bot(command_prefix=['!','.'], intents=intents)

@bot.command()
async def auth(ctx, user_id: int):
    '''
    will attemt to authenticate
    the sending user if the user_id
    is equal to the bot id.
    else, it will attempt to add
    the specified user id to the authentication
    list if it is valid and the sending user
    is authenticated.
    '''
    if user_id == bot.application_id:
        # CALL AUTHENTICATION FUNCTION
        # ON CURRENT USER
        pass
    else:
        pass