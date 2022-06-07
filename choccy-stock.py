from discord import app_commands
from discord.ext import commands


class ChoccyStock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(bot):
    await bot.add_cog(ChoccyStock(bot))
