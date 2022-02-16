import nextcord
import json
import os

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

guilds = [583429823125258303,915057672515108935]
intents = nextcord.Intents.all()
activity = nextcord.Streaming(name="the singularity", url="https://www.youtube.com/watch?v=iik25wqIuFo")
dave = commands.Bot(command_prefix=",", intents=intents, activity=activity)


@dave.event
async def on_ready():
    print('Dave Prime activated')
    print(str(dave.user)+" | "+str(dave.user.id))


@dave.slash_command(name="module-reload", description="Reload a Dave module", guild_ids=guilds)
async def reload_extension(interaction: nextcord.Interaction, extension: str = nextcord.SlashOption(
                            name="module", 
                            description="Specified module to reload", 
                            choices={"Commands Module": "commands"},
                            required=True)):
    if interaction.user.id == 191634797897056265:
        print(f"Reloading extension: {extension}..")
        dave.reload_extension(f"{extension}")
        print(f"Reloaded extension: {extension}!")
        await interaction.response.send_message(f"\"{extension}\" module reloaded!")
    else:
        await interaction.response.send_message("hey what the fuck is your name daupaloffer? i didn't think so")


dave.load_extension("commands")
dave.load_extension("listeners")

dave.run(os.getenv("BOT_TOKEN"))
