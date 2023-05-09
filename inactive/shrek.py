import os
import requests
from discord.ext import commands
from discord.commands import slash_command
from brainbot import guildList


class Shrek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='shrek', description="Turns Brian's light green", guild_ids=guildList)
    async def shrek(self, ctx):
        url = "https://maker.ifttt.com/trigger/shrek/json/with/key/daPGUbt90Z_TJKqQ_IaQPH"
        requests.post(url)
        await ctx.respond("SHEEEESH, you just shrekt Brian")

def setup(bot):
    bot.add_cog(Shrek(bot))