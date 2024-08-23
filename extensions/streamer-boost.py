import discord
from discord.ext import commands


class StreamerBoost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    role_forbidden_message = "Bot doesn't have permission to update roles for this user! Maybe they're higher rank?"

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        # If the member is now streaming
        if (
            any(isinstance(i, discord.Streaming) for i in after.activities)
            and not after.bot
        ):
            streaming_before = any(
                isinstance(i, discord.Streaming) for i in before.activities
            )

            if not streaming_before:
                # print(f"{after.name} is streaming")
                # print(f"before: {before.activities}\nafter: {after.activities}")

                if any(isinstance(i, discord.Streaming) for i in before.activities):
                    print("nevermind they were already streamin")

                streamer_role_id_string = await self.bot.get_cog("DataKeeper").get_guild_data(str(after.guild.id), "streamer_role")
                streamer_role_id = int(streamer_role_id_string)
                streamer_role = after.guild.get_role(streamer_role_id)

                if streamer_role not in after.roles:
                    try:
                        await after.add_roles(
                            streamer_role, reason="Member started streaming"
                        )
                    except discord.errors.Forbidden:
                        print(self.role_forbidden_message)

        # If the member is no longer streaming
        if (
            any(isinstance(i, discord.Streaming) for i in before.activities)
            and not before.bot
        ):
            streaming_after = any(
                isinstance(i, discord.Streaming) for i in after.activities
            )

            if not streaming_after:
                # print(f"{before.name} is no longer streaming")
                # print(f"before: {before.activities}\nafter: {after.activities}")

                if any(isinstance(i, discord.Streaming) for i in after.activities):
                    print("nevermind they still streamin")

                streamer_role_id_string = await self.bot.get_cog("DataKeeper").get_guild_data(str(before.guild.id), "streamer_role")
                streamer_role_id = int(streamer_role_id_string)
                streamer_role = before.guild.get_role(streamer_role_id)

                if streamer_role in before.roles:
                    try:
                        await before.remove_roles(
                            streamer_role, reason="Member stopped streaming"
                        )
                    except discord.errors.Forbidden:
                        print(self.role_forbidden_message)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.sanity()

    async def sanity(self):
        datakeeper = self.bot.get_cog("DataKeeper")
        guild_list = self.bot.guilds

        for g in range(len(guild_list)):
            streamer_role_id_string = await datakeeper.get_guild_data(str(guild_list[g].id), "streamer_role")
            # Don't continue if couldn't get streamer role ID pref
            if not streamer_role_id_string:
                print("Couldn't get streamer role pref for Streamerboost sanity check")
                return

            streamer_role_id = int(streamer_role_id_string)

            if streamer_role_id:
                streamer_role = guild_list[g].get_role(streamer_role_id)
                for m in range(len(guild_list[g].members)):
                    member = guild_list[g].members[m]
                    if any(isinstance(i, discord.Streaming) for i in member.activities):
                        if streamer_role not in member.roles and not member.bot:
                            try:
                                await member.add_roles(
                                    streamer_role, reason="Member is streaming"
                                )
                            except discord.errors.Forbidden:
                                print(self.role_forbidden_message)
                    else:
                        if streamer_role in member.roles:
                            try:
                                await member.remove_roles(
                                    streamer_role, reason="Member is not streaming"
                                )
                            except discord.errors.Forbidden:
                                print(self.role_forbidden_message)


async def setup(bot):
    print("Loading streamer boost extension..")
    await bot.add_cog(StreamerBoost(bot))
