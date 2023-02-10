'''
This is the layer, which is called from the bot events,
it performs validation and calls/directly interfaces with the
functions in the service module
'''
from discord import Interaction
from discord.ext.commands import Context
from distributerbot.service.auth_manager import AuthorityManager
from distributerbot.service.key_manager import KeyManager

'''
     _         _   _                _          _   _             
    / \  _   _| |_| |__   ___  _ __(_)______ _| |_(_) ___  _ __  
   / _ \| | | | __| '_ \ / _ \| '__| |_  / _` | __| |/ _ \| '_ \ 
  / ___ \ |_| | |_| | | | (_) | |  | |/ / (_| | |_| | (_) | | | |
 /_/   \_\__,_|\__|_| |_|\___/|_|  |_/___\__,_|\__|_|\___/|_| |_|
                                                                 
'''


auth_manager = AuthorityManager(auth_file='authorized_users')

def auth_user(ctx: Context, user_id: int) -> str:
    '''
    ** If this is the initial authrization, use the
    server's id as the user_id **
    
    Takes a message context and user_id of user to
    authorize, returns status message and attempts
    to authorize given user
    '''
    caller_id = ctx.author.id
  
    # check if calling user can issue this command
    if auth_manager.has_auth(user_id=caller_id):
        if auth_manager.give_auth(user_id=user_id):
            return f"Success, user with id: {user_id} is now authorized"
        
        # something went wrong while authorizing user
        return f"There was an issue, while authorizing user with id: {user_id}"

    # user issuing command lacks authorization
    return f"Sorry, {ctx.author.name} it appears you're not authorized to issue that command."


def deauth_user(ctx: Context, user_id: int) -> str:
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
## else statement is REQUIRED due to the nature of the asynchronous execution

key_manager = KeyManager('role_defs', 'key_defs', 'keys', 'local_db')

async def set_key(interaction: Interaction, key_type: str,
                  display_name: str, description=''):
    '''
    gets called from modal
    performs set_key functionality, and sends messsage
    to given interaction.response object
    '''
    set_key_status = key_manager.set_key(key_type, display_name, description)
    
    if set_key_status:
        await interaction.response.send_message('Success', ephemeral=True)
    else:
        await interaction.response.send_message('Failed to save key', ephemeral=True)

async def remove_key(interaction: Interaction, key_type: str):
    remove_key_status = key_manager.delete_key(key_type)
    
    if remove_key_status: 
        await interaction.response.send_message('Success', ephemeral=True)
    else:
        await interaction.response.send_message('Failed to remove key', ephemeral=True)

async def set_role(interaction: Interaction, role_name: str, role_keys: str):
    '''
    this takes an interaction(from the modal), a role name,
    and a string of key_types separated by ","s
    '''
    try:
        role_keys = [line.strip() for line in role_keys.split('\n')]
        set_role_status = key_manager.set_role_keys(role_name, role_keys)
    
        if set_role_status:
            await interaction.response.send_message('Success', ephemeral=True)
        else:
            await interaction.response.send_message('Failed to save role', ephemeral=True)
    
    except:
        await interaction.response.send_message('Failed to parse role keys', ephemeral=True)

async def remove_role(interaction: Interaction, role_name: str):
    if key_manager.remove_role(role_name):
        await interaction.response.send_message('Success', ephemeral=True)
    else:
        await interaction.response.send_message('Failed to remove role', ephemeral=True)

async def add_role_key(itneraction: Interaction, role_name: str, key_type: str):
    return

async def remove_role_key(interaction: Interaction, role_name: str, key_type: str):
    return

'''
  _  __          ____       _ _                      
 | |/ /___ _   _|  _ \  ___| (_)_   _____ _ __ _   _ 
 | ' // _ \ | | | | | |/ _ \ | \ \ / / _ \ '__| | | |
 | . \  __/ |_| | |_| |  __/ | |\ V /  __/ |  | |_| |
 |_|\_\___|\__, |____/ \___|_|_| \_/ \___|_|   \__, |
           |___/                               |___/ 
'''
async def get_user_keys(interaction: Interaction):
    user_id = interaction.user.id
    user_keys = key_manager.db_manager.get_user_keys(user_id)
    if not len(user_keys):
        await interaction.response.send_message("You don't have any claimed keys", ephemeral=True)
    else:
        message = ''
        for key in user_keys:
            message += f'{key.display_name}: ||{key.key}||\n ```{key.description}```\n'
            
        await interaction.response.send_message(message, ephemeral=True)
    

async def claim_keys(interaction):
    '''
    check if the user has the appropriate role to claim keys
    check if the user has already claimed keys
    check which keys the user has not claimed
    
    '''
    user_id = interaction.user.id
    member = interaction.guild.get_member(user_id)
    
    available_keys = key_manager.get_user_available_keys(member)

    if available_keys:
        key_manager.give_user_keys(interaction.user, available_keys)

        await get_user_keys(interaction)
    else:
        user_keys = key_manager.db_manager.get_user_keys(user_id)
        if len(user_keys) > 0:
            await get_user_keys(interaction)
        else:
            await interaction.response.send_message('No keys available with your roles', ephemeral=True)