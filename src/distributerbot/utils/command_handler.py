import asyncio
from distributerbot.api.app import authed_users

async def auth_user(user_id: int) -> str:
    if  str(user_id) in authed_users:
        return f'User with id: {user_id} is already authenticated.'

    with open('authed_users.txt', 'a') as txt_authed_users:
        try:
            await txt_authed_users.write(user_id)
            authed_users.append(str(user_id))
            return(f'Authenticated user withid: {user_id}.')
        except Exception as e:
            print(e)
            return f'There was an issue authenticating user.'