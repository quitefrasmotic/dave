import nextcord
from nextcord.ext import commands
from main import guild_ids


class Commands(commands.Cog):
    def __init__(self, dave):
        self.dave = dave

    @nextcord.slash_command(guild_ids=guild_ids)
    async def testcommand(self, interaction):
        await interaction.response.send_message("idiot")

    @nextcord.slash_command(name="owo", description="owo-ify", guild_ids=guild_ids)
    async def owoifier(
        self,
        interaction,
        message: str = nextcord.SlashOption(  # type: ignore - refer to comment in same place in module-commands for explanation
            name="message",
            description="owo-ify provided message instead of previous message",
            required=False,
        ),
        anonymous: bool = nextcord.SlashOption(  # type: ignore
            name="anonymous",
            description="Make it look like it was Dave Prime who sent the message",
            required=False,
        ),
    ):

        if message:
            owo_payload = message
        else:
            owo_payload = (await interaction.channel.history(limit=1).flatten())[0]
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
            await interaction.channel.send(owo_payload)
            await interaction.response.send_message("Message sent!", ephemeral=True)
        else:
            await interaction.response.send_message(owo_payload)


def setup(dave):
    dave.add_cog(Commands(dave))
