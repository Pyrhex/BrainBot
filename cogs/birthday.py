from datetime import date
import datetime
import os
import json
import discord
import mysql.connector

from brainbot import guildList
from discord.ext import commands, tasks
from discord.ext import commands
from discord.commands import slash_command
def getBirthdaysToday():
    pass

class BirthdayReminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders.start()

    def cog_unload(self):
        self.reminders.cancel()
    # @slash_command(name='birthday', description="This will fetch the specified person's birthday", guild_ids=guildList)
    # async def birthday(self, ctx):
    #     today = date.today()
    #     json_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'birthdays.json'))
    #     with open(json_file_path, 'r+') as file:
    #     # First we load existing data into a dict.
    #         file_data = json.load(file)
    #         for i in file_data["birthdays"]:
    #             birthday = date(1999p, i["month"], i["day"])
    #             if(birthday.month == today.month and birthday.day == today.day):
    #                 await ctx.respond("It's " + i["name"] + "'s birthday today!")
    #                 return

    #TODO add new function so you can set a dedicated birthday channel instead of hardcoding it
    @tasks.loop(time=datetime.time(hour=16, minute=0, second=0, tzinfo=datetime.timezone.utc))
    async def reminders(self):
        mydb = mysql.connector.connect(
            host = os.environ.get('SQL_HOST'),
            user = os.environ.get('SQL_USER'),
            password = os.environ.get('SQL_PASS')
        )
        cursor = mydb.cursor()
        today = date.today()
        cursor.execute("USE brainbot")
        cursor.execute(f"SELECT name FROM birthdays where month = {today.month} and day = {today.day}")
        row = cursor.fetchall()
        for [i] in row:
            embed=discord.Embed(title=f"It's {i}'s birthday today!", color=discord.Color.green())
            await self.bot.get_channel(1111494799267209286).send(embed=embed)
        mydb.close()
    @reminders.before_loop
    async def before_reminder(self):
        print('waiting...')
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(BirthdayReminders(bot))