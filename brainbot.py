import asyncio
import discord
import time
import random
from datetime import datetime
from discord.ext import tasks, commands
from datetime import time, timezone


bot = discord.Bot()

guildList=[928169465475133440, 159037207460577281]

@tasks.loop(time=time(2, 0, tzinfo=timezone.utc)) 
async def runCrypto():
    try:
        print("Running crypto scraper...")
        exec(open("CryptoOrganizer/cryptoScraper.py").read())
        print("File run successfully")
    except:
        print("File ran into an error")

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name) 
    print(bot.user.id)
    print('------')
    runCrypto.start()

def is_me(m):
    return m.author == bot.user

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

# @client.command()
# async def coinflip(ctx):
# 	result = ['Heads', 'Tails']
# 	response = random.choice(result)
# 	await ctx.send(response)

# @client.command()
# async def rolldice(ctx):
# 	result = ['1', '2', '3', '4', '5', '6']
# 	response = random.choice(result)
# 	await ctx.send("You rolled a " + response)


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

f = open("discordToken.txt", "r")
key = f.readline().strip()
f.close()
bot.run(key)
