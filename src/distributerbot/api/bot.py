import asyncio
import discord
from discord import Permissions, Interaction
from discord.ext.commands import Bot
from discord.ui import View, Button, TextInput, Item
from distributerbot.views.key_management_views import KeyClaimButton

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.message_content = True

bot = Bot(command_prefix=['!','.'], intents=intents)
from distributerbot.utils import command_handler as ch
from distributerbot.views.key_management_views import SetKeyModal, RemoveKeyModal
from distributerbot.views.role_key_views import SetRoleKeys

NO_PERM = "Sorry, you don't have permission to use that comand"

def is_bot(m):
    return m.author == bot.user
'''
@bot.event
async def on_connect():
    view = View()
    view.add_item(KeyClaimButton())
    
    chat_names = []
    
    try:
        with open('claim_chats.txt', 'r') as chats:
            chat_names = [name.strip('\n') for name in chats.readlines()]
    except Exception as e:
        print("Failed to open claim_chats")
        print(e)
        return
    print(chat_names)
    guilds = bot.guilds
    
    for guild in guilds:
        print(guild.name)
        for chat in chat_names:
            channel = discord.utils.get(guild.text_channels, name=chat)
            print(channel)
            if isinstance(channel, discord.TextChannel):
                try:
                    await channel.purge(limit=10, check=is_bot)
                except:
                    print('failed to purge messages')
                await channel.send('', view=view)
                '''
    # loop thru channel names in channel_name.txt
    # get the guilds that this shard manages
    # loop thru those guilds and try to find a server with the
    # use discord.utils.get(guild.channels, name=)
    # use chat_channel.get_history().flatten

@bot.event
async def on_ready():
    view = View()
    view.add_item(KeyClaimButton())
    
    chat_names = []
    
    try:
        with open('claim_chats.txt', 'r') as chats:
            chat_names = [name.strip('\n') for name in chats.readlines()]
    except Exception as e:
        print("Failed to open claim_chats")
        print(e)
        return
    print(chat_names)
    guilds = bot.guilds
    
    for guild in guilds:
        print(guild.name)
        for chat in chat_names:
            channel = discord.utils.get(guild.text_channels, name=chat)
            print(channel)
            if isinstance(channel, discord.TextChannel):
                try:
                    await channel.purge(limit=10, check=is_bot)
                except:
                    print('failed to purge messages')
                await channel.send('', view=view)
                
    # set permissions
    bot.tree.get_command('setkey').checks = [has_auth_check]
    bot.tree.get_command('removekey').checks = [has_auth_check]
    bot.tree.get_command('setrolekeys').checks = [has_auth_check]
    
    # set handle errors
    
    await bot.tree.sync()

@bot.command(hidden=True)
async def auth(ctx, user_id: int):
    '''
    .auth <user_id> for initial setup, use discord guild id
    '''
    response = ch.auth_user(ctx=ctx, user_id=user_id)
    
    await ctx.reply(response, ephemeral=True)

@bot.command(hidden=True)
async def deauth(ctx, user_id: int):
    '''
    .deauth <user_id>
    '''
    
    response = ch.deauth_user(ctx, user_id)
    
    await ctx.reply(response, ephemeral=True)

@bot.command(hidden=True)
async def getmyid(ctx):
    await ctx.reply(f'{ctx.author.id}', ephemeral=True)

@bot.command(hidden=True)
async def createbutton(ctx):
    view = View()
    btn = KeyClaimButton()
    view.add_item(btn)
    await ctx.send('', view=view)


## KEY MANAGEMENT
@bot.tree.command(name='keys')
async def keys(interaction):
    '''
    this checks the amount of keys that are left
    and returns a status message with the name of the key
    and the amount that are available
    '''
    return
@bot.tree.command(name='claim')
async def claim(interaction):
    await ch.claim_keys(interaction)

@bot.tree.command(name='setkey')
async def setkey(interaction):
    modal = SetKeyModal()
    await interaction.response.send_modal(modal)

@bot.tree.command(name='removekey')
async def removekey(interaction, key_name: str):
    await ch.remove_key(interaction, key_name)



## ROLE KEY MANAGEWMENT
@bot.tree.command(name='setrolekeys')
async def setrolekeys(interaction):
    modal = SetRoleKeys()
    
    await interaction.response.send_modal(modal)

@bot.tree.command(name='removerole')
async def removerole(interaction):    
    return

### AUTH CHECK: Feeds into command.checks: [coroutine]
async def has_auth_check(interaction: Interaction):
    has_auth = ch.auth_manager.has_auth(interaction.user.id)
    if not has_auth:
        await interaction.response.send_message(NO_PERM, ephemeral=True)

    return has_auth

async def error_callback(interaction):
    message = 'Something went wrong while processing your request'
    await interaction.response.send_message(message, ephemeral=True)