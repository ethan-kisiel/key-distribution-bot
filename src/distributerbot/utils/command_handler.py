'''
This is the layer, which is called from the bot events,
it performs validation and calls/directly interfaces with the
functions in the service module
'''
from discord.ext.commands import Context
from distributerbot.service.auth_manager import AuthorityManager


'''
     _         _   _                _          _   _             
    / \  _   _| |_| |__   ___  _ __(_)______ _| |_(_) ___  _ __  
   / _ \| | | | __| '_ \ / _ \| '__| |_  / _` | __| |/ _ \| '_ \ 
  / ___ \ |_| | |_| | | | (_) | |  | |/ / (_| | |_| | (_) | | | |
 /_/   \_\__,_|\__|_| |_|\___/|_|  |_/___\__,_|\__|_|\___/|_| |_|
                                                                 
'''


auth_manager = AuthorityManager(auth_file='authorized_users')

async def auth_user(ctx: Context, user_id: int) -> str:
    '''
    ** If this is the initial authrization, use the
    server's id as the user_id **
    
    Takes a message context and user_id of user to
    authorize, returns status message and attempts
    to authorize given user
    '''
    caller_id = ctx.author.id
    
    # flow for initial authoriazation using server id
    if user_id == ctx.guild.id:
        if auth_manager.give_auth(caller_id):
            # successful initial authorization
            return f"Success, {ctx.author.name}, you are now authorized."

        #unsuccessful initial auth
        return f"Something went wrong"
      
    # check if calling user can issue this command
    if auth_manager.has_auth(user_id=caller_id):
        if auth_manager.give_auth(user_id=user_id):
            return f"Success, user with id: {user_id} is now authorized"
        
        # something went wrong while authorizing user
        return f"There was an issue, while authorizing user with id: {user_id}"

    # user issuing command lacks authorization
    return f"Sorry, {ctx.author.name} it appears you're not authorized to issue that command."


async def deauth_user(ctx: Context, user_id: int) -> str:
    '''
    Takes message context and user_id of user to
    deauthorize, returns a status message after
    attempting to deauthorize user.
    '''
    caller_id = ctx.author.id
    
    # check if calling user can issue this command
    if auth_manager.has_auth(user_id=caller_id):
        if auth_manager.has_auth(user_id=user_id):
            if auth_manager.remove_auth(user_id=user_id):
                return f"Success, user with id: {user_id} has been deauthorized."
            
            # something went wrong while deauthorizing user
            return f"There was an issue deauthorizing user with id: {user_id}"
        
        # user doesn't appear in authorization list
        return f"It appears that user isn't authorized."

    # user issuing command lacks authorization
    return f"Sorry, {ctx.author.name} it appears you're not authorized to issue that command."


'''
  _  __          __  __                                                   _   
 | |/ /___ _   _|  \/  | __ _ _ __   __ _  __ _  ___ _ __ ___   ___ _ __ | |_ 
 | ' // _ \ | | | |\/| |/ _` | '_ \ / _` |/ _` |/ _ \ '_ ` _ \ / _ \ '_ \| __|
 | . \  __/ |_| | |  | | (_| | | | | (_| | (_| |  __/ | | | | |  __/ | | | |_ 
 |_|\_\___|\__, |_|  |_|\__,_|_| |_|\__,_|\__, |\___|_| |_| |_|\___|_| |_|\__|
           |___/                          |___/                               
'''










'''
  _  __          ____       _ _                      
 | |/ /___ _   _|  _ \  ___| (_)_   _____ _ __ _   _ 
 | ' // _ \ | | | | | |/ _ \ | \ \ / / _ \ '__| | | |
 | . \  __/ |_| | |_| |  __/ | |\ V /  __/ |  | |_| |
 |_|\_\___|\__, |____/ \___|_|_| \_/ \___|_|   \__, |
           |___/                               |___/ 
'''