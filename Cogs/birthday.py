import datetime
import os
import json
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
    @tasks.loop(time=datetime.time(hour=16, minute=0, second=0, tzinfo=datetime.timezone.utc))
    async def reminders(self):
        # today = date.today()
        # json_file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', 'data', 'birthdays.json'))
        # with open(json_file_path, 'r+') as file:
        # # First we load existing data into a dict.
        #     file_data = json.load(file)
        #     for i in file_data["birthdays"]:
        #         birthday = date(1999, i["month"], i["day"])
        #         if(birthday.month == today.month and birthday.day == today.day):
        #             print("It's " + i["name"] + "'s birthday today!")
        #             return
        print("hi")
def setup(bot):
    bot.add_cog(BirthdayReminders(bot))