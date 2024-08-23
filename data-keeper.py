import discord
import json
import os.path

from discord import app_commands
from discord.ext import commands
from typing import Optional, Literal, get_args


# This is now less dumb, but still really needs to be replaced with an actual database
class DataKeeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    guild_keys = Literal["streamer_role", "admin_channel"]
    member_keys = Literal["temp"]

    pref_cmd_group = app_commands.Group(
        name="preferences", description="Set your Dave Prime preferences"
    )
    # preferences_group_show = app_commands.Group(name="show", description="Show your current Dave Prime preferences", parent=preferences_group)

    @pref_cmd_group.command(name="set", description="Change Dave Prime preferences")
    @app_commands.describe(
        streamer_role="This is the role the Streamerboost feature will give to members that are streaming",
        admin_channel="This is the channel that Dave Prime will send moderation alerts",
    )
    @app_commands.rename(
        streamer_role="streamer-boost-role", admin_channel="admin-channel"
    )
    async def set_guild_pref(
        self,
        interaction: discord.Interaction,
        streamer_role: Optional[discord.Role],
        admin_channel: Optional[discord.TextChannel],
    ):
        prefs_changed = False
        if streamer_role:
            await self.set_guild_data(str(interaction.guild_id), "streamer_role", str(streamer_role.id))
            prefs_changed = True
        if admin_channel:
            await self.set_guild_data(str(interaction.guild_id), "admin_channel", str(admin_channel.id))
            prefs_changed = True

        if prefs_changed:
            response_message = "Preferences updated!"
        else:
            response_message = "Select an option to change a preference!"

        await interaction.response.send_message(response_message, ephemeral=True)

    @pref_cmd_group.command(
        name="show", description="Show current Dave Prime preferences"
    )
    async def show_guild_pref(self, interaction: discord.Interaction):
        #fix this to get all keys with new method
        prefs = await self.get_guild_data(str(interaction.guild_id), "admin_channel")
        prefs.pop("members", None)

        await interaction.response.send_message(prefs, ephemeral=True)

    async def load_data(self):
        # Check if data file exists, if not create new one and generate basic json structure
        if os.path.isfile("data.json"):
            data = open("data.json", "r+")
            json_data = json.load(data)
        else:
            data = open("data.json", "w+")
            json_data = {
                "data": {
                    "guilds": []
                }
            }
            data.seek(0)
            data.write(json.dumps(json_data, indent=4))
            data.truncate()
        return data, json_data

    async def initialise_guild(self, json_data, guild: str):
        in_list = None
        for i in json_data["data"]["guilds"]:
            if i["guild"] == guild:
                in_list = True

        if not in_list:
            json_data["data"]["guilds"].append(
                {
                    "guild": guild,
                    "members": []
                }
            )
        return json_data

    async def write_data(self, data, json_data):
        # Go to beginning of file and truncate to overwrite file to avoid opening file twice with different modes
        data.seek(0)
        data.write(json.dumps(json_data, indent=4))
        data.truncate()
        data.close()

    async def set_guild_data(self, guild: str, key: guild_keys, value: str):
        data, json_data = await self.load_data()

        json_data = await self.initialise_guild(json_data, guild)

        for i in json_data["data"]["guilds"]:
            if i["guild"] == guild:
                i[key] = value

        await self.write_data(data, json_data)

    async def set_member_data(self, guild: str, user: str, key: member_keys, value: str):
        data, json_data = await self.load_data()

        json_data = await self.initialise_guild(json_data, guild)

        for i in json_data["data"]["guilds"]:
            if i["guild"] == guild:
                member_exists = None
                for j in i["members"]:
                    if j["member"] == user:
                        j[key] = value
                        member_exists = True

                if not member_exists:
                    i["members"].append({"member": user, key: value})

        await self.write_data(data, json_data)

    '''async def get_guild_data(self, guild: str):
        data, json_data = await self.load_data()

        prefs = None
        for i in json_data["data"]["guilds"]:
            if i["guild"] == guild:
                prefs = i
        return prefs'''

    async def get_guild_data(self, guild: str, key: guild_keys):
        data, json_data = await self.load_data()
        data.close()

        value = None
        for i in json_data["data"]["guilds"]:
            if i["guild"] == guild:
                value = i[key]
        return value

    async def get_member_data(self, guild: str, user: str, key: member_keys):
        data, json_data = await self.load_data()
        data.close()

        value = None
        for i in json_data["data"]["guilds"]:
            if i["guild"] == guild:
                for j in i["members"]:
                    if j["member"] == user:
                        value = j[key]
        return value


async def setup(bot):
    print("Loading data keeper extension..")
    await bot.add_cog(DataKeeper(bot))
