import discord
import os

import time
from discord.ext import commands

role_forbidden_message = "Bot doesn't have permission to update roles for this user! Maybe they're higher rank?"

admin_channel_id = int(os.getenv("ADMIN_CHANNEL", ""))
if not admin_channel_id:
    print("Please provide an admin channel snowflake in your .env!")
    raise SystemExit


@commands.Cog.listener()
async def listeny(ctx):
    if str(ctx.content) == "hey" and not ctx.author.bot:
        await ctx.channel.send("hey")


class StreamerBoost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        # If the member is now streaming
        if any(isinstance(i, discord.Streaming) for i in after.activities):
            streaming_before = any(
                isinstance(i, discord.Streaming) for i in before.activities
            )

            if not streaming_before:
                print(f"{after.name} is streaming")
                print(f"before: {before.activities}\nafter: {after.activities}")

                if any(isinstance(i, discord.Streaming) for i in before.activities):
                    print("nevermind they were already streamin")

                streamer_role = discord.Object(
                    943381405801533471
                )  # Stop hardcoding this - store in a better way

                if streamer_role not in after.roles:
                    try:
                        await after.add_roles(
                            streamer_role, reason="Member started streaming"
                        )
                    except discord.errors.Forbidden:
                        print(role_forbidden_message)

        # If the member is no longer streaming
        if any(isinstance(i, discord.Streaming) for i in before.activities):
            streaming_after = any(
                isinstance(i, discord.Streaming) for i in after.activities
            )

            if not streaming_after:
                print(f"{before.name} is no longer streaming")
                print(f"before: {before.activities}\nafter: {after.activities}")

                if any(isinstance(i, discord.Streaming) for i in after.activities):
                    print("nevermind they still streamin")

                streamer_role = discord.Object(943381405801533471)

                if streamer_role in before.roles:
                    try:
                        await before.remove_roles(
                            streamer_role, reason="Member stopped streaming"
                        )
                    except discord.errors.Forbidden:
                        print(role_forbidden_message)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.sanity()

    async def sanity(self):
        # This is awful and I will endeavour to improve this ASAP
        main_guild = ""
        for i in range(len(self.bot.guilds)):
            if self.bot.guilds[i].name == "repository of stuff":
                main_guild = self.bot.guilds[i]
        if main_guild == "":
            raise SystemExit

        streamer_role = main_guild.get_role(943381405801533471)

        for m in range(len(main_guild.members)):
            if any(
                isinstance(i, discord.Streaming)
                for i in main_guild.members[m].activities
            ):
                if streamer_role not in main_guild.members[m].roles:
                    try:
                        await main_guild.members[m].add_roles(
                            streamer_role, reason="Member is streaming"
                        )
                    except discord.errors.Forbidden:
                        print(role_forbidden_message)
            else:
                if streamer_role in main_guild.members[m].roles:
                    try:
                        await main_guild.members[m].remove_roles(
                            streamer_role, reason="Member is not streaming"
                        )
                    except discord.errors.Forbidden:
                        print(role_forbidden_message)


class ModerationWatcher(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Timeout watcher
    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if after.is_timed_out() and not before.is_timed_out():
            timeout_until_unix = int(after.timed_out_until.timestamp())  # type: ignore
            now_unix = int(time.time())
            description = f"{after.mention} was just timed out until <t:{timeout_until_unix}:f> \
                            \nOccurred <t:{now_unix}:f>"

            # If I want timestamp back, the precise way to provide it is "datetime.datetime.now(datetime.timezone.utc)"
            timeout_embed = discord.Embed(
                title=f"Moderation Alert: TIME OUT",
                color=discord.Colour.from_rgb(255, 171, 246),
                description=description,
            )
            timeout_embed.set_thumbnail(url=after.display_avatar.url)

            admin_channel = self.bot.get_channel(admin_channel_id)
            if isinstance(admin_channel, discord.TextChannel):
                await admin_channel.send(embed=timeout_embed)

    # Ban watcher
    @commands.Cog.listener()
    async def on_member_ban(self, guild: discord.Guild, user: discord.Member):
        ban_embed = discord.Embed(
            title=f"Moderation Alert: BAN",
            color=discord.Colour.from_rgb(255, 171, 246),
            description=f"{user.mention} has been banned from the server \nOccurred <t:{int(time.time())}:f>",
        )
        ban_embed.set_thumbnail(url=user.display_avatar.url)

        admin_channel = self.bot.get_channel(admin_channel_id)
        if isinstance(admin_channel, discord.TextChannel):
            await admin_channel.send(embed=ban_embed)

    # Unban watcher
    @commands.Cog.listener()
    async def on_member_unban(self, guild: discord.Guild, user: discord.Member):
        unban_embed = discord.Embed(
            title=f"Moderation Alert: UNBAN",
            color=discord.Colour.from_rgb(255, 171, 246),
            description=f"{user.mention} has been unbanned from the server \nOccurred <t:{int(time.time())}:f>",
        )
        unban_embed.set_thumbnail(url=user.display_avatar.url)

        admin_channel = self.bot.get_channel(admin_channel_id)
        if isinstance(admin_channel, discord.TextChannel):
            await admin_channel.send(embed=unban_embed)


async def setup(bot):
    print("Loading listeners extension..")
    bot.add_listener(listeny, "on_message")
    await bot.add_cog(StreamerBoost(bot))
    await bot.add_cog(ModerationWatcher(bot))
