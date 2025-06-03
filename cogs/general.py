import discord
import asyncio
import os
import mysql.connector
import math

from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command
from dadjokes import Dadjoke


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='ping', description="Ping a user multiple times", guild_ids=guildList)
    async def ping(self, ctx, username, message="null"):
        if ctx.author.id != 184861751169384449:
            await ctx.respond(content=username)
            for i in range(4):
                message = await ctx.send(content=username)
                await asyncio.sleep(1)
        else:
            await ctx.respond("https://tenor.com/view/get-rekt-stewie-family-guy-gif-11461913")

    @slash_command(name='schedule', description="This will display Brian's current class schedule", guild_ids=guildList)
    async def schedule(self, ctx):
        embed=discord.Embed(title="Brian's School Schedule", description="This is the updated school schedule for Summer 2023", color=0x00ff1e)
        embed.add_field(name="Monday", value="No classes", inline=False)
        embed.add_field(name="Tuesday", value="No classes", inline=False)
        embed.add_field(name="Wednesday", value="No classes", inline=True)
        embed.add_field(name="Thursday", value="CMPT475 (AQ3149) 11:30AM - 2:20PM", inline=False)
        embed.add_field(name="Friday", value="No classes", inline=True)
        await ctx.respond(ephemeral=True, embeds=[embed])

    @slash_command(name='clear', description='This will clear the number of messages specified', guild_ids=guildList)
    async def clear(self, ctx: discord.ApplicationContext, amount: int):
        print("Clear command triggered")

        await ctx.defer(ephemeral=True)
        deleted = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(description=f"✅ Deleted {len(deleted)} messages.")
        await ctx.followup.send(embed=embed, ephemeral=True)
    @slash_command(name="dadjoke", description="This will display a random dad joke", guild_ids=guildList)
    async def dadjoke(self, ctx):
        dadjoke = Dadjoke()
        await ctx.respond(dadjoke.joke)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        else:
            mydb = mysql.connector.connect(
            host = os.environ.get('SQL_HOST'),
            user = os.environ.get('SQL_USER'),
            password = os.environ.get('SQL_PASS')
            )
            cursor = mydb.cursor()
            cursor.execute("USE brainbot")
            cursor.execute(f"""INSERT IGNORE INTO user(user_id, username, level, xp, xp_to_next_level) VALUES (%s, %s, 0, 0, 5)""", (message.author.id, message.author.name,))
            # insert into table if user doesn't exist
            cursor.execute(f"""UPDATE user SET xp = xp + 1 WHERE username = %s""", (message.author.name,))
            cursor.execute(f"""SELECT xp, xp_to_next_level, level FROM user WHERE username = %s""", (message.author.name,))
            row = cursor.fetchone()
            xp = row[0]
            xp_to_next_level = row[1]
            level = row[2]
            # addXP()
            if(xp >= xp_to_next_level):
                level = level + 1
                xp = xp - xp_to_next_level
                xp_to_next_level = math.ceil(xp_to_next_level * 1.2)
                embed = discord.Embed(title=f":tada: Congrats! {message.author.display_name} is now level {level}. :tada:", color=5763719)
                await message.channel.send(embed=embed)
            cursor.execute(f"""UPDATE user SET xp = %s, xp_to_next_level = %s, level = %s WHERE username = %s""", (xp, xp_to_next_level, level, message.author.name,))
            # cursor.execute(f"""REPLACE INTO server (user_id, username, level, xp, xp_to_next_level) VALUES(%s, %s, %s, %s, %s);""", (message.author.id, message.author.name, vods_channel.id, vods_channel.name))
            mydb.commit()
            mydb.close()

def setup(bot):
    bot.add_cog(General(bot))