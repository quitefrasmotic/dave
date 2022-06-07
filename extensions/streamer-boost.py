import discord
import os
from discord.ext import commands

admin_channel_id = int(os.getenv("ADMIN_CHANNEL", ""))
if not admin_channel_id:
    print("Please provide an admin channel snowflake in your .env!")
    raise SystemExit

role_forbidden_message = "Bot doesn't have permission to update roles for this user! Maybe they're higher rank?"


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


async def setup(bot):
    print("Loading streamer boost extension..")
    await bot.add_cog(StreamerBoost(bot))
