import nextcord
from nextcord.ext import commands


class slash_commands(commands.Cog):
    def __init__(self, dave):
        self.dave = dave
    
    @nextcord.slash_command(name="module-reload", description="Reload a Dave module", guild_ids=self.dave.guild_ids)
    async def reload_extension(self, interaction, 
                            extension: str = nextcord.SlashOption(name="module", description="Specified module to reload", choices={"Commands Module": "commands"}, required=True)):
        
        if interaction.user.id == 191634797897056265:
            print(f"Reloading extension: {extension}..")
            self.dave.reload_extension(f"{extension}")
            print(f"Reloaded extension: {extension}!")
            await interaction.response.send_message(f"\"{extension}\" module reloaded!")
        else:
            await interaction.response.send_message("hey what the fuck is your name daupaloffer? i didn't think so")


def setup(dave):
    dave.add_cog(slash_commands(dave))
