import os
from discord.ext import commands
from discord.commands import slash_command
from brainbot import guildList


class YoutubeMP3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='download2mp3', description="Converts the Youtube video into an MP3 file", guild_ids=guildList)
    async def convert(self, ctx):
        pass

def setup(bot):
    bot.add_cog(YoutubeMP3(bot))