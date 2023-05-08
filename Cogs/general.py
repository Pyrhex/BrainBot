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
        embed=discord.Embed(title="Brian's School Schedule", description="This is the updated school schedule for Summer 2023", color=0x00ff1e)
        embed.add_field(name="Monday", value="No classes", inline=False)
        embed.add_field(name="Tuesday", value="No classes", inline=False)
        embed.add_field(name="Wednesday", value="11:30AM - 12:20PM", inline=True)
        embed.add_field(name="Thursday", value="11:30AM - 2:00PM", inline=False)
        embed.add_field(name="Friday", value="10:30AM - 12:20PM", inline=True)
        await ctx.respond(ephemeral=True, embeds=[embed])

    @slash_command(name='clear', description='This will clear the number of messages specified', guild_ids=guildList)
    async def clear(self, ctx, amount: int):
        deleted = await ctx.channel.purge(limit=amount)
        embed = discord.Embed(description=f"✅ Deleted {len(deleted)} messages.")
        await ctx.respond(ephemeral=True, embed=embed)

def setup(bot):
    bot.add_cog(General(bot))