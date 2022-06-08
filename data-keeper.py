"""import sqlite3

con = sqlite3.connect("database.db")
cursor = con.cursor()

if cursor.execute("")"""
import discord
import json

from typing import Optional
from typing import Literal
from discord import app_commands
from discord.ext import commands


class DataKeeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    pref_cmd_description = "Change Dave Prime preferences"
    pref_option_description = [
        "This is the role the StreamerBoost feature will give to members that are streaming"
    ]

    @app_commands.command(name="preferences", description=pref_cmd_description)
    @app_commands.describe(streamer_role=pref_option_description[0])
    @app_commands.rename(streamer_role="streamerboost-role")
    async def save_prefs(
        self, interaction: discord.Interaction, streamer_role: Optional[discord.Role]
    ):
        data = open("data.json", "r+")
        in_array = None
        json_data = json.load(data)

        for i in json_data["data"]["guilds"]:
            if i["guild"] == str(interaction.guild_id):
                in_array = True

        if not in_array:
            json_data["data"]["guilds"].append({"guild": str(interaction.guild_id), "streamer_role": str(streamer_role.id)}) # Linter complains about this - will fix underlying cause
        else:
            for guild_element in json_data["data"]["guilds"]:
                if guild_element["guild"] == str(interaction.guild_id):
                    json_data["data"]["guilds"][guild_element]["streamer_role"] = str(streamer_role.id)

        data.seek(0)
        data.write(json.dumps(json_data, indent=4, sort_keys=True))
        data.truncate()
        data.close()

        await interaction.response.send_message("Preference updated!")


    pref_list = Literal["streamer_role"]

    async def get_prefs(self, guild: int, pref: pref_list):
        data = open("data.json", "r")
        json_data = json.load(data)

        result = None
        for guild_element in json_data["data"]["guilds"]:
            if guild_element["guild"] == str(guild):
                result = guild_element[pref]

        return result
        # [obj for obj in json_data["data"]["guilds"] if obj["guild"]==str(guild)][0][pref]
        # match pref:
        #    case "streamer_role":
        #        return [obj for obj in json_data["data"]["guilds"] if obj["guild"]==guild][0]["streamer_role"]
        #    case _:
        #        raise Exception("Invalid pref input")


async def setup(bot):
    print("Loading data keeper extension..")
    await bot.add_cog(DataKeeper(bot))
