import discord
import os
import random
import openai

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

    gpt_timeout = False

    async def setup_hook(self):
        await self.load_extension("module-management")
        await self.load_extension("data-keeper")
        await self.load_extension("extensions.commands")
        await self.load_extension("extensions.listeners")
        await self.load_extension("extensions.moderation-watcher")
        await self.load_extension("extensions.streamer-boost")

        openai.api_key = os.getenv("OPENAI_KEY")


load_dotenv()

test_env = os.getenv("TEST_ENV", "false").lower() == "true"

guild_vars = ["MAIN_GUILD", "TEST_GUILD"]
guild_ids = [os.getenv(i, "") for i in guild_vars]
if not any(guild_ids):
    print("Please provide guild IDs in your .env!")
    raise SystemExit

if test_env:
    guild = guild_ids[1]
else:
    guild = guild_ids[0]
guild_object = discord.Object(guild)

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
    print("---------")
    print("Dave Prime activated")
    print(f"{bot.user} | {bot.application_id}\n")


# Manual app command sync
@bot.event
async def on_message(ctx):
    if str(ctx.content) == "DAVE sync" and ctx.author.id == 191634797897056265:
        await ctx.channel.send("Syncing commands..")
        try:
            bot.tree.copy_global_to(guild=guild_object)
            await bot.tree.sync(guild=guild_object)
            await ctx.channel.send("Synced")
        except discord.errors.HTTPException:
            await ctx.channel.send("Failed to sync - probably reached daily limit")

    await bot.process_commands(ctx)

bot_token = str(os.getenv("BOT_TOKEN", ""))
if bot_token:
    bot.run(bot_token)
else:
    print("Please provide a bot token in your .env!")
    raise SystemExit
