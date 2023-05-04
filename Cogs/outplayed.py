import os
import requests
import discord
import time
import asyncio
import json
from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command

def addToServerJson(server):
    print()

    with open(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'servers.json')),'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["servers"].append(server)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

class Outplayed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='vods', description="Sets the vod/clips channel", guild_ids=guildList)
    async def vods(self, ctx, channel: discord.TextChannel):
        #TODO add channel id to database with guild id as key
        server = {"server id": ctx.guild.id, "server name": ctx.guild.name, "vods channel": channel.id}
        addToServerJson(server)
        await ctx.respond("Set vods channel to " + channel.mention)
    @commands.Cog.listener()
    async def on_message(self, message):
        
        print(message.channel.guild.name)
        print(message.channel.guild.id)
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