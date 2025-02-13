import discord
import asyncio
import mysql.connector
import datetime
import os

from brainbot import guildList
from discord.ext import commands, tasks
from discord.commands import slash_command

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
class Labubu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders.start()

    def cog_unload(self):
        self.reminders.cancel()
    @tasks.loop(minutes=1)
    async def reminders(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Runs Chrome in headless mode
        chrome_options.add_argument("--no-sandbox")  # Prevents sandboxing issues
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcomes limited resource issues in Docker or virtual environments
        chrome_options.add_argument("--remote-debugging-port=9222")  # Open remote debugging port for Chrome
        chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (needed for headless mode on some systems)

        # Initialize the WebDriver with the specified options
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the webpage
        try:
            driver.get("https://www.popmart.com/ca/products/2084/THE-MONSTERS-COCA-COLA-SERIES-Vinyl-Face-Blind-Box")  # Replace with the actual URL of the page

        # Wait for the page to load (optional, you can adjust the time as needed)
            driver.implicitly_wait(10)  # Waits for up to 10 seconds
        except Exception as e:
            print("Unable to load page, will try again in 1 minute")

        try:
            # Locate the "ADD TO BAG" button using different locators:
            add_to_bag_button = driver.find_element(By.XPATH, "//*[text()='NOTIFY ME WHEN AVAILABLE']")
            now = datetime.datetime.now()
            print(f"OUT OF STOCK AS OF {now}")
        except Exception as e:
            channel = self.bot.get_channel(1338405956270428220)
            embed = discord.Embed(description=f"Item has been restocked")
            await channel.send(embed=embed)

        # Close the WebDriver after actions are complete
        driver.quit()
    @reminders.before_loop
    async def before_reminder(self):
        print(f'Starting up Popmart alerts')
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(Labubu(bot))