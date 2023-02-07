from discord import ui
from discord import TextStyle, Interaction


class CustomRoleSelect(ui.RoleSelect):
    
    disabled = False
    
    async def callback(self, interaction: Interaction):
        await interaction.response.send_message(f'selected')


class Questionnaire(ui.Modal, title='Questionnaire Response'):
    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=TextStyle.paragraph)

    #role_select = CustomRoleSelect()
    
    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
        
