import datetime
from discord.ext import commands, tasks

utc = datetime.timezone.utc

# If no tzinfo is given then UTC is assumed.
times = [
    datetime.time(hour=8, tzinfo=utc),
]

class BirthdayReminders(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders.start()

    def cog_unload(self):
        self.reminders.cancel()

    @tasks.loop(time=times)
    async def reminders(self):
        pass