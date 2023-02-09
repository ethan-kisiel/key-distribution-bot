import asyncio
import discord
from discord import Permissions, Interaction
from discord.ext.commands import Bot
from discord.ui import View, Button, TextInput, Item

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

# slash commands
@bot.event
async def on_ready():
    # set permissions
    bot.tree.get_command('setkey').checks = [has_auth_check]
    bot.tree.get_command('removekey').checks = [has_auth_check]
    bot.tree.get_command('setrolekeys').checks = [has_auth_check]
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
    await ch.user_keys(interaction)


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
        await interaction.response.send_message(NO_PERM)

    return has_auth