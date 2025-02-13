import discord
import asyncio
import os
import math

from brainbot import guildList
from discord.ext import commands
from discord.commands import slash_command
from email_validator import validate_email, EmailNotValidError

class EmailVerifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='verify', description="Verifies an email", guild_ids=[928169465475133440])
    async def verify(self, ctx, email):
        try:
            emailinfo = validate_email(email, check_deliverability=True)
            await ctx.respond("Email deliverable")
        except EmailUndeliverableError as e:
            await ctx.respond("Email not deliverable")
            # print("Email not deliverable")

def setup(bot):
    bot.add_cog(EmailVerifier(bot))