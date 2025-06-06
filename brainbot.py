import asyncio
import discord
import time
import random
# import rigCheck
import requests
import os
import argparse
import logging

from datetime import datetime
from discord.ext import tasks
from datetime import time, timezone

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--debug", help="debug mode", action=argparse.BooleanOptionalAction)
args = parser.parse_args()

intents = discord.Intents.all()
intents.message_content = True
bot = discord.Bot(intents=intents, activity=discord.Activity(type=discord.ActivityType.listening, name="your convos"))

if(args.debug == True):
    guildList = [928169465475133440]
    key = os.environ.get('DISCORD_TOKEN_DEBUG')
else:
    guildList = [928169465475133440, 159037207460577281,913881236441821324]
    key = os.environ.get('DISCORD_TOKEN')
    
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) 
    print(bot.user.id)
    print('------')

def is_me(m):
    return m.author == bot.user

@bot.slash_command(name='reload', description='This will reload the cog', guild_ids=guildList)
async def reload(self, cog_name):
    try:
        self.bot.reload_extension(f"cogs.{cog_name}")
        await ctx.respond(f"{cog_name} cog has been reloaded", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"Error reloading {cog_name}: {e}", ephemeral=True)

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

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(key)
