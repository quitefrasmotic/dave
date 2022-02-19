import nextcord
import datetime
import os

from time import mktime
from nextcord.ext import commands
from main import dave

role_forbidden_message = "Bot doesn't have permission to update roles for this user! Maybe they're higher rank?"

admin_channel_id = int(os.getenv("ADMIN_CHANNEL", ""))
if not admin_channel_id:
    print("Please provide an admin channel snowflake in your .env!")
    raise SystemExit


@commands.Cog.listener()
async def on_ready():
    await streamerboost_sanity(dave)


@commands.Cog.listener()
async def listeny(ctx):
    if str(ctx.content) == "hey" and not ctx.author.bot:
        await ctx.channel.send("hey")


@commands.Cog.listener()
async def streamerboost(before, after):
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

            streamer_role = after.guild.get_role(943381405801533471)

            if streamer_role not in after.roles:
                try:
                    await after.add_roles(
                        streamer_role, reason="Member started streaming"
                    )
                except nextcord.errors.Forbidden:
                    print(role_forbidden_message)

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

            streamer_role = before.guild.get_role(943381405801533471)

            if streamer_role in before.roles:
                try:
                    await before.remove_roles(
                        streamer_role, reason="Member stopped streaming"
                    )
                except nextcord.errors.Forbidden:
                    print(role_forbidden_message)


async def streamerboost_sanity(dave):
    main_guild = ""
    for i in range(len(dave.guilds)):
        if dave.guilds[i].name == "The Waifu Corner":
            main_guild = dave.guilds[i]
    if main_guild == "":
        raise SystemExit

    streamer_role = main_guild.get_role(943381405801533471)

    for h in range(len(main_guild.humans)):
        if any(
            isinstance(i, nextcord.Streaming) for i in main_guild.humans[h].activities
        ):
            if streamer_role not in main_guild.humans[h].roles:
                try:
                    await main_guild.humans[h].add_roles(
                        streamer_role, reason="Member is streaming"
                    )
                except nextcord.errors.Forbidden:
                    print(role_forbidden_message)
        else:
            if streamer_role in main_guild.humans[h].roles:
                try:
                    await main_guild.humans[h].remove_roles(
                        streamer_role, reason="Member is not streaming"
                    )
                except nextcord.errors.Forbidden:
                    print(role_forbidden_message)


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
    dave.add_listener(on_ready, "on_ready")
