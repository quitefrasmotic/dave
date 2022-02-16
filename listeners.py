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
    # Sometimes they don't have an activity, so only do this if they do
    if after.activity:
        if after.activity.type == nextcord.ActivityType.streaming and before.activity.type != nextcord.ActivityType.streaming:
            print(str(after.name)+" is streaming")
            print(str(after.activity.details)+" "+str(after.activity.game))
            if after.guild == 915057672515108935:
                await after.add_roles([943381405801533471], reason="Member started streaming")
    
    if before.activity:
        if before.activity.type == nextcord.ActivityType.streaming and after.activity.type != nextcord.ActivityType.streaming:
            print(str(before.name)+" is no longer streaming")
            print(str(after.activity.details)+" "+str(after.activity.game))
            if before.guild == 915057672515108935:
                await before.remove_roles([943381405801533471], reason="Member stopped streaming")


def setup(dave):
    dave.add_listener(listeny, "on_message")
    dave.add_listener(streamerboost, "on_presence_update")
