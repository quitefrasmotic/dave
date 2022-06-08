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
        await self.load_extension("module-management")
        await self.load_extension("extensions.commands")
        await self.load_extension("extensions.listeners")
        await self.load_extension("extensions.moderation-watcher")
        await self.load_extension("extensions.streamer-boost")

        guild_object = discord.Object(guild)
        self.tree.copy_global_to(guild=guild_object)
        await self.tree.sync(guild=guild_object)


load_dotenv()

test_env = bool(os.getenv("TEST_ENV", ""))
if not test_env:
    print("Please clarify if this is a test environment in your .env!")
    raise SystemExit

guild_vars = ["MAIN_GUILD", "TEST_GUILD"]
guild_ids = [os.getenv(i, "") for i in guild_vars]
if not any(guild_ids):
    print("Please provide guild IDs in your .env!")
    raise SystemExit

if test_env:
    guild = guild_ids[1]
else:
    guild = guild_ids[0]

with open("activitylinks", "r") as f:
    links = f.readlines()
    activity_link = random.choice(links)
    f.close()

command_prefix = ","
intents = discord.Intents.all()
activity = discord.Streaming(name="the singularity", url=activity_link)

bot = DaveBot(command_prefix=command_prefix, intents=intents, activity=activity)


@bot.event
async def on_ready():
    print("Dave Prime activated")
    print(f"{bot.user} | {bot.application_id}\n")


bot_token = str(os.getenv("BOT_TOKEN", ""))
if bot_token:
    bot.run(bot_token)
else:
    print("Please provide a bot token in your .env!")
    raise SystemExit
