import discord
import asyncio
import mysql.connector
import datetime
import os

from brainbot import guildList
from discord.ext import commands, tasks
from discord.commands import slash_command
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def getFlavours():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://earnesticecream.com/locations/fraser-st/")
    elem = driver.find_element(by=By.ID, value="id_first")
    return elem.text.split("\n")
def getIcecreamChannel(guild_id):
    mydb = mysql.connector.connect(
            host = os.environ.get('SQL_HOST'),
            user = os.environ.get('SQL_USER'),
            password = os.environ.get('SQL_PASS')
    )
    cursor = mydb.cursor()
    cursor.execute("USE brainbot")
    cursor.execute(f"""SELECT icecream_channel_id FROM server WHERE id = %s;""", (guild_id,))
    row = cursor.fetchone()[0]
    mydb.close()
    return row

class Earnest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders.start()

    def cog_unload(self):
        self.reminders.cancel()
    @slash_command(name='flavour', description='gets the current updated flavour list for Earnest Ice Cream Fraser location', guild_ids=[913881236441821324])
    async def flavours(self, ctx):
        await ctx.defer()
        flavours = getFlavours()
        regular=discord.Embed(title="Earnest Ice Cream", description="Regular Flavours", color=0xFF5733)
        vegan=discord.Embed(title="", description="Vegan Flavours", color=0x00FF00)
        for i in flavours:
            if("Vegan" in i):
                vegan.add_field(name=f":icecream: {i}", value="", inline=False)
            else:
                regular.add_field(name=f":ice_cream: {i}", value="", inline=True)
        current = datetime.datetime.now()
        vegan.set_footer(text=f"Updated at: {current}")
        await ctx.respond(embeds=[regular, vegan])
    @tasks.loop(time=datetime.time(hour=22, minute=30, second=0, tzinfo=datetime.timezone.utc))
    async def reminders(self):
        # await ctx.defer()
        flavours = getFlavours()
        regular=discord.Embed(title="Earnest Ice Cream", description="Regular Flavours", color=0xFF5733)
        vegan=discord.Embed(title="", description="Vegan Flavours", color=0x00FF00)
        for i in flavours:
            if("Vegan" in i):
                vegan.add_field(name=f":icecream: {i}", value="", inline=False)
            else:
                regular.add_field(name=f":ice_cream: {i}", value="", inline=True)
        current = datetime.datetime.now()
        vegan.set_footer(text=f"Updated at: {current}")
        # get ice cream channel
        channel = self.bot.get_channel(getIcecreamChannel(913881236441821324))
        await channel.send(embeds=[regular, vegan])

    @reminders.before_loop
    async def before_reminder(self):
        print(f'Starting up Earnest Ice Cream reminders...')
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(Earnest(bot))