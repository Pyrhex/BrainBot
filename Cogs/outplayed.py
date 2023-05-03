import os
import requests
import discord
import time
import asyncio
from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command

class Outplayed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='vods', description="Sets the vod/clips channel", guild_ids=guildList)
    async def vods(self, ctx, channel):
        #TODO add channel id to database with guild id as key
        pass

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        if user == self.bot.user:
            return
        if("https://outplayed.tv/media/" in message.content):
            link = message.content.split()[-1]
            caption =" ".join(message.content.split()[:-1])
            embed=discord.Embed(title="Outplayed.tv", url=link, color=0xFF5733)
            embed.add_field(name="User", value=user, inline=False)
            embed.add_field(name="Caption", value=caption, inline=False)
            embed.set_thumbnail(url=str(user.display_avatar.url))
            channel = self.bot.get_channel(980554422277013574)
            await channel.send(embed=embed)
            await channel.send(link)
            await message.delete()
        

def setup(bot):
    bot.add_cog(Outplayed(bot))