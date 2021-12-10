import nextcord
from nextcord.activity import Streaming
from nextcord.ext import commands
from nextcord.ext.commands import context
from nextcord.types.activity import ActivityType


@commands.Cog.listener()
async def listeny(ctx):
    if str(ctx.content) == "hey" and not ctx.author.bot:
        await ctx.channel.send("hey")


@commands.Cog.listener()
async def streamerboost(before, after):
    if after.activity:
        if after.activity.type == nextcord.ActivityType.streaming:
            print(str(after.name)+" is streaming")


def setup(dave):
    dave.add_listener(listeny, "on_message")
    dave.add_listener(streamerboost, "on_presence_update")
