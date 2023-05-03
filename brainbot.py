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

intents = discord.Intents.all()
intents.message_content = True
bot = discord.Bot(intents=intents)

guildList = [928169465475133440, 159037207460577281, 913881236441821324]

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) 
    print(bot.user.id)
    print('------')

def is_me(m):
    return m.author == bot.user

# @bot.slash_command(name='rigs', description="fetches the current rigs and their current hashrates", guild_ids=guildList)
# async def rigs(ctx):
#     await ctx.defer()
#     if ctx.author.id == 188765438446927873:
#         embed=discord.Embed(title="Current Rigs", description="This is the rigs running and their current hashrate", color=0x00ff1e)
#         rigs = rigCheck.getRigs()
#         for key in rigs:
#             embed.add_field(name=key, value=rigs[key], inline=False)
#         await ctx.respond(embeds=[embed])
#     else:
#         await ctx.respond("You do not have permission to use this command!")

for filename in os.listdir("./Cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"Cogs.{filename[:-3]}")

f = open("discordToken.txt", "r")
key = f.readline().strip()
f.close()
bot.run(key)
