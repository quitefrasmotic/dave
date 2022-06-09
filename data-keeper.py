import discord
import json
import os.path

from discord import app_commands
from discord.ext import commands
from typing import Optional, Literal, get_args


class DataKeeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pref_cmd_description = "Change Dave Prime preferences"
    pref_list = Literal["streamer_role"]
    pref_option_description = [
        "This is the role the Streamerboost feature will give to members that are streaming",
        "This is the channel that Dave Prime will send moderation alerts",
    ]
    pref_cmd_group = app_commands.Group(
        name="preferences", description="Set your Dave Prime preferences"
    )
    # preferences_group_show = app_commands.Group(name="show", description="Show your current Dave Prime preferences", parent=preferences_group)

    @pref_cmd_group.command(name="set", description=pref_cmd_description)
    @app_commands.describe(
        streamer_role=pref_option_description[0],
        admin_channel=pref_option_description[1],
    )
    @app_commands.rename(
        streamer_role="streamer-boost-role", admin_channel="admin-channel"
    )
    async def save_prefs(
        self,
        interaction: discord.Interaction,
        streamer_role: Optional[discord.Role],
        admin_channel: Optional[discord.TextChannel],
    ):
        # Check if data file exists, if not create new one and generate basic json structure
        if os.path.isfile("data.json"):
            data = open("data.json", "r+")
            json_data = json.load(data)
        else:
            data = open("data.json", "w+")
            json_data = {"data": {"guilds": []}}

        # Check if guild is already in the data, update value if so
        in_array = None
        for guild in json_data["data"]["guilds"]:
            if guild["guild"] == interaction.guild_id:
                if streamer_role:
                    guild["streamer_role"] = streamer_role.id

                if admin_channel:
                    guild["admin_channel"] = admin_channel.id

                in_array = True

        # If guild isn't in data, add new entry into guild array with values
        if not in_array:
            json_data["data"]["guilds"].append(
                {
                    "guild": interaction.guild_id,
                    "streamer_role": streamer_role.id if streamer_role else None,
                    "admin_channel": admin_channel.id if admin_channel else None,
                }
            )

        # Go to beginning of file and truncate to overwrite file to avoid opening file twice with different modes
        data.seek(0)
        data.write(json.dumps(json_data, indent=4, sort_keys=True))
        data.truncate()
        data.close()

        await interaction.response.send_message("Preferences updated!", ephemeral=True)

    @pref_cmd_group.command(
        name="show", description="Show current Dave Prime preferences"
    )
    async def show_prefs(self, interaction: discord.Interaction):
        pref_list_args = get_args(self.pref_list)

        pref_values = []
        for i in range(len(pref_list_args)):
            value = await self.get_prefs(interaction.guild_id, pref_list_args[i])  # type: ignore
            pref_values.append(f'"{pref_list_args[i]}": "{value}"')

        pref_values_string = "\n".join(pref_values)
        await interaction.response.send_message(pref_values_string, ephemeral=True)

    async def get_prefs(self, guild: int, pref: pref_list):
        try:
            data = open("data.json", "r")
        except FileNotFoundError:
            print("Data file not found!")
            return None

        json_data = json.load(data)

        result = None
        for guild_element in json_data["data"]["guilds"]:
            if guild_element["guild"] == guild:
                result = guild_element[pref]

        return result


async def setup(bot):
    print("Loading data keeper extension..")
    await bot.add_cog(DataKeeper(bot))
