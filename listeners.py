from discord.ext import commands


class BasicListeners(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if str(ctx.content) == "hey" and not ctx.author.bot:
            await ctx.channel.send("hey")


async def setup(bot):
    print("Loading listeners extension..")
    await bot.add_cog(BasicListeners(bot))
