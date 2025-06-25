import discord
import requests
import datetime
import os
import re
import pandas as pd
import pytz
import traceback

from discord.ext import commands
from discord.commands import slash_command
from discord import option

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import upload_schedule



SCOPES = ["https://www.googleapis.com/auth/calendar"]

class WorkScheduler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='upload', description="Uploads work schedule to Google Calendar", guild_ids=[928169465475133440])
    @option("attachment", discord.Attachment, description="Excel file (.xlsx)", required=False)
    async def upload(self, ctx, attachment: discord.Attachment):
        if not attachment:
            await ctx.respond("You didn't give me a file to upload! :sob:")
            return
        await ctx.defer()
        try:
            response = requests.get(attachment.url)
            upload_schedule(response)
            await ctx.respond(f"✅ Schedule uploaded successfully from file: `{attachment.filename}`")

        except Exception as e:
            print(traceback.format_exc())
            await ctx.respond(f"❌ An error occurred:\n```\n{str(e)}\n```")

def setup(bot):
    bot.add_cog(WorkScheduler(bot))
