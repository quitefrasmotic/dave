import nextcord
from nextcord.ext import commands

guilds = [583429823125258303,915057672515108935]


class slash_commands(commands.Cog):
    def __init__(self, dave):
        self.dave = dave
    
    @nextcord.slash_command(guild_ids=guilds)
    async def testcommand(self, interaction):
        await interaction.response.send_message("idiot")


def setup(dave):
    dave.add_cog(slash_commands(dave))
