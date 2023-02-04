'''
This is the layer, which is called from the bot events,
it performs validation and calls/directly interfaces with the
functions in the service module
'''
from discord.ext.commands import Context
from distributerbot.service.auth_manager import AuthorityManager
from distributerbot.api.bot import bot

auth_manager = AuthorityManager(auth_file='authorized_users.txt')

async def auth_user(ctx: Context, user_id: int) -> str:
    caller_id = ctx.author.id
    
    # flow for initial authoriazation using bot id
    if user_id == bot.application_id:
        if auth_manager.give_auth(caller_id):
            # successful initial authorization
            return f"Success, {ctx.author.name}, you are now authorized."
        else:
            #unsuccessful initial auth
            return f"Something went wrong"
      
    # check if calling user can issue this command
    if auth_manager.has_auth(user_id=caller_id):
        if auth_manager.give_auth(user_id=user_id):
            return f"Success, user with id: {user_id} is now authorized"
        return f"There was an issue, while authorizing user with id: {user_id}"

    return f"Sorry, {ctx.author.name} it appears you're not authorized to issue that command."