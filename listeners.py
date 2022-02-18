import nextcord
import datetime
import os

from time import mktime
from nextcord.ext import commands
from main import dave

currently_streaming = []


admin_channel_id = int(os.getenv("ADMIN_CHANNEL", ""))
if not admin_channel_id:
    print("Please provide an admin channel snowflake in your .env!")
    raise SystemExit


@commands.Cog.listener()
async def listeny(ctx):
    if str(ctx.content) == "hey" and not ctx.author.bot:
        await ctx.channel.send("hey")


@commands.Cog.listener()
async def streamerboost(before, after):
    """for i in range(len(after.activities)):
    if after.activities[i].type == nextcord.ActivityType.streaming:
        print("FOUND IT")"""

    # If the member is now streaming
    if any(isinstance(i, nextcord.Streaming) for i in after.activities):
        streaming_before = any(
            isinstance(i, nextcord.Streaming) for i in before.activities
        )

        if not streaming_before:
            print(str(after.name) + " is streaming")
            print(
                "before: " + str(before.activities) + " after: " + str(after.activities)
            )

            if any(isinstance(i, nextcord.Streaming) for i in before.activities):
                print("nevermind they were already streamin")

            if after.id == 915057672515108935:
                await after.add_roles(
                    [943381405801533471], reason="Member started streaming"
                )
                currently_streaming.append(after.id)

    # If the member is no longer streaming
    if any(isinstance(i, nextcord.Streaming) for i in before.activities):
        streaming_after = any(
            isinstance(i, nextcord.Streaming) for i in after.activities
        )

        if not streaming_after:
            print(str(before.name) + " is no longer streaming")
            print(
                "before: " + str(before.activities) + " after: " + str(after.activities)
            )

            if any(isinstance(i, nextcord.Streaming) for i in after.activities):
                print("nevermind they still streamin")

            if before.id == 915057672515108935:
                await before.remove_roles(
                    [943381405801533471], reason="Member stopped streaming"
                )
                currently_streaming.remove(before.id)


"""async def streamerboost_cleanup(dave):
    if currently_streaming:
        for i in range(len(currently_streaming)-1, -1, -1): # Count backwards to stop it from getting confused if a list element is popped
            member = dave.get_member(currently_streaming[i])
            if member.activity.type != nextcord.ActivityType.streaming:
                currently_streaming.pop(i)
                await member.remove_roles([943381405801533471], reason="Removed by cleanup")"""


@commands.Cog.listener()
async def timeout_watcher(before, after):
    if after.timeout:
        description = f"**{after.mention} was just TIMED OUT until <t:{int(mktime(after.timeout.timetuple()))}:f>** \
                        \n*Occurred: <t:{int(mktime(datetime.datetime.now().timetuple()))}:f>*"

        # If I want timestamp back, the precise way to provide it is "datetime.datetime.now(datetime.timezone.utc)"
        timeout_embed = nextcord.Embed(
            title=f"Moderation Alert - TIME OUT - {after.name}#{after.discriminator}",
            color=nextcord.Colour.from_rgb(255, 171, 246),
            description=description,
        )
        timeout_embed.set_thumbnail(url=after.display_avatar.url)

        admin_channel = dave.get_channel(admin_channel_id)
        if isinstance(admin_channel, nextcord.TextChannel):
            await admin_channel.send(embed=timeout_embed)


@commands.Cog.listener()
async def ban_watcher(guild, user):
    ban_embed = nextcord.Embed(
        title=f"Moderation Alert - BAN - {user.name}#{user.discriminator}",
        color=nextcord.Colour.from_rgb(255, 171, 246),
        description=f"**{user.mention} has been BANNED from the server** \n*Occurred: <t:{int(mktime(datetime.datetime.now().timetuple()))}:f>*",
    )
    ban_embed.set_thumbnail(url=user.display_avatar.url)

    admin_channel = dave.get_channel(admin_channel_id)
    if isinstance(admin_channel, nextcord.TextChannel):
        await admin_channel.send(embed=ban_embed)


@commands.Cog.listener()
async def unban_watcher(guild, user):
    unban_embed = nextcord.Embed(
        title=f"Moderation Alert - UNBAN - {user.name}#{user.discriminator}",
        color=nextcord.Colour.from_rgb(255, 171, 246),
        description=f"**{user.mention} has been UNBANNED from the server** \n*Occurred: <t:{int(mktime(datetime.datetime.now().timetuple()))}:f>*",
    )
    unban_embed.set_thumbnail(url=user.display_avatar.url)

    admin_channel = dave.get_channel(admin_channel_id)
    if isinstance(admin_channel, nextcord.TextChannel):
        await admin_channel.send(embed=unban_embed)


def setup(dave):
    dave.add_listener(listeny, "on_message")
    dave.add_listener(streamerboost, "on_presence_update")
    dave.add_listener(timeout_watcher, "on_member_update")
    dave.add_listener(ban_watcher, "on_member_ban")
    dave.add_listener(unban_watcher, "on_member_unban")

    # streamerboost_cleanup(dave)
