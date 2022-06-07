from discord import app_commands
from discord.ext import commands
from typing import Literal


class ModuleManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="module-reload", description="Reload a Dave module")
    @app_commands.describe(extension="Specified module to reload")
    async def reload_extension(
        self, interaction, extension: Literal["commands", "listeners"]
    ):
        if interaction.user.id == 191634797897056265:
            print(f'Reloading extension "{extension}"..')
            await self.bot.reload_extension(extension)
            print(f'Reloaded extension "{extension}"!')
            await interaction.response.send_message(f'"{extension}" module reloaded!')
        else:
            await interaction.response.send_message(
                "hey what the fuck is your name daupaloffer? i didn't think so"
            )


async def setup(bot):
    print("Loading module management extension..")
    await bot.add_cog(ModuleManagement(bot))
