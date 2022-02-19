import nextcord
from nextcord.ext import commands
from main import guild_ids


class ChoccyStock(commands.Cog):
    def __init__(self, dave):
        self.dave = dave
    
def setup(dave):
    dave.add_cog(ChoccyStock(dave))
