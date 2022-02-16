import nextcord
import datetime
import os

from time import mktime
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
    try:
        if after.activity:
            if after.activity.type == nextcord.ActivityType.streaming and before.activity.type != nextcord.ActivityType.streaming:
                print(str(after.name)+" is streaming")
                print(str(after.activity.details))
                if after.guild == 915057672515108935:
                    await after.add_roles([943381405801533471], reason="Member started streaming")
    except AttributeError:
        print(after + "NoneType on after")
        pass
    
    try:
        if before.activity:
            if before.activity.type == nextcord.ActivityType.streaming and after.activity.type != nextcord.ActivityType.streaming:
                print(str(before.name)+" is no longer streaming")
                print(str(after.activity.details))
                if before.guild == 915057672515108935:
                    await before.remove_roles([943381405801533471], reason="Member stopped streaming")
    except AttributeError:
        print(before + "NoneType on before")
        pass


@commands.Cog.listener()
async def timeout_watcher(before, after):
    if after.timeout:
        description = f"**{after.mention} was just TIMED OUT until <t:{int(mktime(after.timeout.timetuple()))}:f>** \
                        \n*Occurred: <t:{int(mktime(datetime.datetime.now().timetuple()))}:f>*"
        
        # If I want timestamp back, the precise way to provide it is "datetime.datetime.now(datetime.timezone.utc)"
        timeout_embed = nextcord.Embed(title=f":timer: Moderation Alert - TIME OUT - {after.name}#{after.discriminator}",
                                       color=nextcord.Colour.from_rgb(255,171,246),
                                       description=description)

        timeout_embed.set_thumbnail(url=after.display_avatar.url)
        await admin_channel.send(embed=timeout_embed)


@commands.Cog.listener()
async def ban_watcher(guild, user):
    ban_embed = nextcord.Embed(title=f":hammer: Moderation Alert - BAN - {user.name}#{user.discriminator}",
                               color=nextcord.Colour.from_rgb(255,171,246),
                               description=f"**{user.mention} has been BANNED from the server** \n*Occurred: <t:{int(mktime(datetime.datetime.now().timetuple()))}:f>*")
    
    ban_embed.set_thumbnail(url=user.display_avatar.url)
    await admin_channel.send(embed=ban_embed)


@commands.Cog.listener()
async def unban_watcher(guild, user):
    unban_embed = nextcord.Embed(title=f":tada: Moderation Alert - UNBAN - {user.name}#{user.discriminator}",
                                 color=nextcord.Colour.from_rgb(255,171,246),
                                 description=f"**{user.mention} has been UNBANNED from the server** \n*Occurred: <t:{int(mktime(datetime.datetime.now().timetuple()))}:f>*")
    
    unban_embed.set_thumbnail(url=user.display_avatar.url)
    await admin_channel.send(embed=unban_embed)


def setup(dave):
    global admin_channel
    admin_channel = dave.get_channel(int(os.getenv("ADMIN_CHANNEL")))
    
    dave.add_listener(listeny, "on_message")
    dave.add_listener(streamerboost, "on_presence_update")
    dave.add_listener(timeout_watcher, "on_member_update")
    dave.add_listener(ban_watcher, "on_member_ban")
    dave.add_listener(unban_watcher, "on_member_unban")
