from discord import ui
from discord import TextStyle
from distributerbot.utils.command_handler import set_role
from distributerbot.utils.command_handler import remove_role

class SetRoleKeys(ui.Modal, title='Set Role Keys'):
    role_name = ui.TextInput(label='Role Name')
    
    role_keys = ui.TextInput(label='Role Keys', style=TextStyle.paragraph)
    
    async def on_submit(self, interaction):
        rn = self.role_name.value
        rk = self.role_keys.value
        await set_role(interaction, rn, rk)
    
    async def on_error(interaction):
        interaction.response.send_message('Sorry, we encountered an error')
        

class RemoveRole(ui.Modal, title='Remove Role'):
    role_name = ui.TextInput(label='Role Name')
    
    async def on_submit(self, interaction):
        rn = self.role_name.value
        await remove_role(interaction, rn)
    
    async def on_error(interaction):
        interaction.response.send_message('Sorry, we encountered an error')