import nextcord
from nextcord.ext import commands


@commands.command()
async def testcommand(ctx):
    await ctx.reply("idiot")


def setup(dave):
    dave.add_command(testcommand)
