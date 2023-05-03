import os
import requests
import discord
import time
import asyncio
from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command


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
        embed=discord.Embed(title="Brian's School Schedule", description="This is the updated school schedule for Spring 2022", color=0x00ff1e)
        embed.add_field(name="Monday", value="TBD", inline=False)
        embed.add_field(name="Tuesday", value="TBD", inline=False)
        embed.add_field(name="Wednesday", value="TBD", inline=True)
        embed.add_field(name="Thursday", value="TBD", inline=False)
        embed.add_field(name="Friday", value="TBD", inline=True)
        await ctx.respond(embeds=[embed])

    @slash_command(name='clear', description='This will clear the number of messages specified', guild_ids=guildList)
    async def clear(self, ctx, amount):
        await ctx.channel.purge(limit=int(amount))
        await ctx.channel.respond(content="Messages Removed")

def setup(bot):
    bot.add_cog(General(bot))