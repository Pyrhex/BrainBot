import os
import discord
import time
import asyncio
import re
import mysql.connector
from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command

def addToDatabase(guild, vods_channel):
    mydb = mysql.connector.connect(
            host = os.environ.get('SQL_HOST'),
            user = os.environ.get('SQL_USER'),
            password = os.environ.get('SQL_PASS')
    )
    cursor = mydb.cursor()
    cursor.execute("USE brainbot")
    cursor.execute(f"""REPLACE INTO server (id, name, vods_channel_id, vods_channel_name) VALUES(%s, %s, %s, %s);""", (guild.id, guild.name, vods_channel.id, vods_channel.name))
    mydb.commit()
    mydb.close()

def getVodsChannel(guild_id):
    mydb = mysql.connector.connect(
            host = os.environ.get('SQL_HOST'),
            user = os.environ.get('SQL_USER'),
            password = os.environ.get('SQL_PASS')
    )
    cursor = mydb.cursor()
    cursor.execute("USE brainbot")
    cursor.execute(f"""SELECT vods_channel_id FROM server WHERE id = %s;""", (guild_id,))
    row = cursor.fetchone()[0]
    mydb.close()
    return row

class Outplayed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='vods', description="Sets the vod/clips channel", guild_ids=guildList)
    async def vods(self, ctx, channel: discord.ForumChannel | discord.TextChannel):
        addToDatabase(ctx.guild, channel)
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
            caption =" ".join(message.content.split()[:-1])
            if(caption == ""):
                caption = "N/A"
            embed=discord.Embed(title="Outplayed.tv", url=link, color=0xFF5733)
            embed.add_field(name="User", value=user.display_name, inline=False)
            embed.add_field(name="Caption", value=caption, inline=False)
            embed.set_thumbnail(url=str(user.display_avatar.url))
            #TODO get the channel from the json file
            try:
                channel = self.bot.get_channel(getVodsChannel(message.guild.id))
                if(channel.type == discord.enums.ChannelType.forum):
                    thread = await channel.create_thread(name=f"{user.display_name}'s Outplayed Clip",auto_archive_duration=60, embed=embed)
                    await thread.send(content=link)
                else:
                    await channel.send(embed=embed)
                    await channel.send(link)
                await message.delete()
            except Exception as e:
                embed=discord.Embed(title=f'An error has occurred: {e}', color=0xFF5733)
                await message.channel.send(embed=embed)
        

def setup(bot):
    bot.add_cog(Outplayed(bot))