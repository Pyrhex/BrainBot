import os
import requests
import discord
import time
import asyncio
import json
import re
from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command

def addToServerJson(server_dict):
    json_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'servers.json'))
    with open(json_file_path, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        
        # Check if server already exists in the file_data.
        for i, server in enumerate(file_data["servers"]):
            if server.keys() == server_dict.keys():
                if server != server_dict:
                    file_data["servers"][i][list(server.keys())[0]]['vods channel'] = server_dict[list(server_dict.keys())[0]]['vods channel']
                break
        else: 
            file_data["servers"].append(server_dict)

        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent=4)
def getVodsChannel(guild_id):
    json_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'servers.json'))
    with open(json_file_path, 'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        for server in file_data["servers"]:
            if str(guild_id) in list(server.keys()):
                return server[str(guild_id)]['vods channel']
        return None
class Outplayed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='vods', description="Sets the vod/clips channel", guild_ids=guildList)
    async def vods(self, ctx, channel: discord.ForumChannel | discord.TextChannel):
        server = {str(ctx.guild.id) : {"server name": ctx.guild.name, "vods channel": channel.id}}
        addToServerJson(server)

        await ctx.respond("Set vods channel to " + channel.mention)
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        if(message.author.bot):
            return
        if user == self.bot.user:
            return  
        
        if("https://outplayed.tv/media/" in message.content):
            link = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
            print(link)
            caption =" ".join(message.content.split()[:-1])
            embed=discord.Embed(title="Outplayed.tv", url=link, color=0xFF5733)
            embed.add_field(name="User", value=user, inline=False)
            embed.add_field(name="Caption", value=caption, inline=False)
            embed.set_thumbnail(url=str(user.display_avatar.url))
            #TODO get the channel from the json file
            try:
                channel = self.bot.get_channel(getVodsChannel(message.guild.id))
                if(channel.type == discord.enums.ChannelType.forum):
                    thread = await channel.create_thread(name=f"{message.author.nick}'s Outplayed Clip",auto_archive_duration=60, embed=embed)
                    await thread.send(content=link)
                else:
                    await channel.send(embed=embed)
                    await channel.send(link)
                await message.delete()
            except Exception as e:
                await message.channel.send(e)
        

def setup(bot):
    bot.add_cog(Outplayed(bot))