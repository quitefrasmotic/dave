import discord
from discord import app_commands
from discord.ext import commands


class BasicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test_command", description="This is a test command")
    async def testcommand(self, interaction: discord.Interaction):
        await interaction.response.send_message("idiot")

    @app_commands.command(name="owo", description="owo-ify your message")
    @app_commands.describe(
        message="Provide a message to be owo-ified instead of using previous message",
        anonymous="Make it look like it was Dave Prime who sent the message",
    )
    async def owoifier(
        self,
        interaction: discord.Interaction,
        message: str = "",
        anonymous: bool = False,
    ):
        if message:
            owo_payload = message
        else:
            message_history = interaction.channel.history(limit=1)  # type: ignore
            owo_payload = [message async for message in message_history][0]

            if not owo_payload.content:  # Maybe add owo_payload.author.bot too
                await interaction.response.send_message("try again, idiot")
                return
            else:
                owo_payload = owo_payload.content

        chars_to_replace = "lrLR"
        for i in chars_to_replace:
            if i.islower():
                owo_payload = owo_payload.replace(i, "w")
            else:
                owo_payload = owo_payload.replace(i, "W")

        if anonymous:
            await interaction.channel.send(owo_payload)  # type: ignore
            await interaction.response.send_message("Message sent!", ephemeral=True)
        else:
            await interaction.response.send_message(owo_payload)


async def setup(bot):
    print("Loading commands extension..")
    await bot.add_cog(BasicCommands(bot))
