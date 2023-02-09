from discord import ui, Embed
from discord import TextStyle, InteractionMessage, SelectOption
from distributerbot.utils.command_handler import set_key
from distributerbot.utils.command_handler import remove_key

class SetKeyModal(ui.Modal, title='Set Key'):
    key_type = ui.TextInput(label='Key Type')
    display_name = ui.TextInput(label='Display Name')
    description = ui.TextInput(label='Description', style=TextStyle.paragraph)
    
    async def on_submit(self, interaction):
        await set_key(interaction, self.key_type.value,
                      self.display_name.value, self.description.value)
        
        
        
class RemoveKeyModal(ui.Modal, title='Remove Key'):
    key_type = ui.TextInput(label='Key')
    
    async def on_submit(self, interaction):
        await remove_key(interaction, self.key_type.value)
