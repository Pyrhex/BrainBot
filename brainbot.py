import asyncio
import discord
import time
import random
import rigCheck
import requests
import os
from datetime import datetime
from discord.ext import tasks
from datetime import time, timezone


bot = discord.Bot()

guildList=[928169465475133440, 159037207460577281, 913881236441821324]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) 
    print(bot.user.id)
    print('------')
    # runCrypto.start()

def is_me(m):
    return m.author == bot.user

@bot.slash_command(guild_ids=guildList)  # create a slash command for the supplied guilds
async def hello(ctx):
    await ctx.respond(f"Hello {ctx.author}!")

@bot.slash_command(name='ping', description="Ping a user multiple times", guild_ids=guildList)
async def ping(ctx, username, message="null"):
    if ctx.author.id != 184861751169384449:
        await ctx.respond(content=username)
        for i in range(5):
            message = await ctx.send(content=username)
            time.sleep(1)
            deleted = await ctx.channel.purge(limit=1, check=is_me(message))
    else:
        await ctx.respond("https://tenor.com/view/get-rekt-stewie-family-guy-gif-11461913")

@bot.slash_command(name='rigs', description="fetches the current rigs and their current hashrates", guild_ids=guildList)
async def rigs(ctx):
    await ctx.defer()
    if ctx.author.id == 188765438446927873:
        embed=discord.Embed(title="Current Rigs", description="This is the rigs running and their current hashrate", color=0x00ff1e)
        rigs = rigCheck.getRigs()
        for key in rigs:
            embed.add_field(name=key, value=rigs[key], inline=False)
        await ctx.respond(embeds=[embed])
    else:
        await ctx.respond("You do not have permission to use this command!")

@bot.slash_command(name='schedule', description="This will display Brian's current class schedule", guild_ids=guildList)
async def schedule(ctx):
    embed=discord.Embed(title="Brian's School Schedule", description="This is the updated school schedule for Spring 2022", color=0x00ff1e)
    embed.add_field(name="Monday", value="12:30 PM - 1:20 PM", inline=False)
    embed.add_field(name="Tuesday", value="No Classes", inline=False)
    embed.add_field(name="Wednesday", value="12:30 PM - 1:20 PM", inline=True)
    embed.add_field(name="Thursday", value="No Classes", inline=False)
    embed.add_field(name="Friday", value="12:30 PM - 1:20 PM", inline=True)
    await ctx.respond(embeds=[embed])

@bot.slash_command(name='clear', description='This will clear the number of messages specified', guild_ids=guildList)
async def clear(ctx, amount):
    await ctx.channel.purge(limit=int(amount))
    await ctx.channel.respond(content="Messages Removed")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

f = open("discordToken.txt", "r")
key = f.readline().strip()
f.close()
bot.run(key)
