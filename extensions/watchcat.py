import discord
import time
import os
from discord.ext import commands

class Watchcat(commands.Cog):
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

            datakeeper = self.bot.get_cog("DataKeeper")
            admin_channel_id = int(await datakeeper.get_guild_data(str(after.guild.id), "admin_channel"))

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

        datakeeper = self.bot.get_cog("DataKeeper")
        admin_channel_id = int(await datakeeper.get_guild_data(str(guild.id), "admin_channel"))

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

        datakeeper = self.bot.get_cog("DataKeeper")
        admin_channel_id = await datakeeper.get_guild_data(guild.id, "admin_channel")

        admin_channel = self.bot.get_channel(admin_channel_id)
        if isinstance(admin_channel, discord.TextChannel):
            await admin_channel.send(embed=unban_embed)


async def setup(bot):
    print("Loading moderation watcher extension..")
    await bot.add_cog(Watchcat(bot))
