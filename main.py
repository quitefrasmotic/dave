import discord
import os
import random

from discord.ext import commands
from dotenv import load_dotenv


class DaveBot(commands.Bot):
    def __init__(
        self,
        command_prefix: str,
        intents: discord.Intents,
        activity: discord.BaseActivity,
    ):
        super().__init__(
            command_prefix=command_prefix, intents=intents, activity=activity
        )

    async def setup_hook(self):
        await self.load_extension("commands")
        # await self.load_extension("listeners")
        # await self.load_extension("module-commands")
        # await self.load_extension("choccy-stock")

        self.tree.copy_global_to(guild=test_guild)
        await self.tree.sync(guild=test_guild)


load_dotenv()
with open("activitylinks", "r") as f:
    links = f.readlines()
    activity_link = random.choice(links)
    f.close()

guild_ids = [583429823125258303, 915057672515108935]
test_guild = discord.Object(guild_ids[1])

command_prefix = ","
intents = discord.Intents.all()
activity = discord.Streaming(name="the singularity", url=activity_link)

bot = DaveBot(command_prefix=command_prefix, intents=intents, activity=activity)


@bot.event
async def on_ready():
    print("Dave Prime activated")
    print(f"{bot.user} | {bot.application_id}")


bot_token = str(os.getenv("BOT_TOKEN", ""))
if bot_token:
    bot.run(bot_token)
else:
    print("Please provide a bot token in your .env!")
    raise SystemExit
