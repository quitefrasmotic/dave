import nextcord
from nextcord.ext import commands


@commands.Cog.listener()
async def listeny(ctx):
    if str(ctx.content) == "hey" and not ctx.author.bot:
        await ctx.channel.send("hey")


def setup(dave):
    dave.add_listener(listeny, "on_message")
