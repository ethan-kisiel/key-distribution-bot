from discord import ui
from discord import Interaction

class CustomView(ui.View):

    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()
        
    async def interaction_check(self, interaction: Interaction, /) -> bool:
        await interaction.response.send_message('Interacted')