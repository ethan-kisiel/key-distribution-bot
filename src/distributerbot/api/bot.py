import asyncio
import discord
from discord.ext.commands import Bot
from discord.ui import View, Button

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.guild_messages = True
intents.message_content = True

bot = Bot(command_prefix=['!','.'], intents=intents)
from distributerbot.utils.command_handler import auth_user

# slash commands

@bot.event
async def on_ready():
    await bot.tree.sync()
    
@bot.tree.command(name='claim')
async def claim(ctx):
    return

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
    response = await auth_user(ctx=ctx, user_id=user_id)
    
    await ctx.reply(response, ephemeral=True)
    

async def button_callback(ctx):
    print("Pressed")

@bot.command()
async def button(ctx):

    view = View()
    button = Button(label='button')
    button.callback = button_callback
    view.add_item(button)
    
    
    await ctx.send(view=view)
    
