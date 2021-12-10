import nextcord
import json
import os

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = nextcord.Intents.default()
dave = commands.Bot(command_prefix=",", intents=intents)


@dave.event
async def on_ready():
    print('Dave Prime activated')
    print(str(dave.user)+" | "+str(dave.user.id))


dave.load_extension("commands")
dave.load_extension("listeners")

dave.run(os.getenv("BOT_TOKEN"))
