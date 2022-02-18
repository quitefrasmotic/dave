import nextcord
import os
import random

from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
with open("activitylinks", "r") as f:
    links = f.readlines()
    activity_link = random.choice(links)
    f.close()

guild_ids = [583429823125258303, 915057672515108935]
intents = nextcord.Intents.all()
activity = nextcord.Streaming(name="the singularity", url=activity_link)
dave = commands.Bot(command_prefix=",", intents=intents, activity=activity)


@dave.event
async def on_ready():
    print("Dave Prime activated")
    print(str(dave.user) + " | " + str(dave.application_id))


dave.load_extension("commands")
dave.load_extension("listeners")
dave.load_extension("module-commands")

bot_token = str(os.getenv("BOT_TOKEN", ""))
if bot_token:
    dave.run(bot_token)
else:
    print("Please provide a bot token in your .env!")
    raise SystemExit
