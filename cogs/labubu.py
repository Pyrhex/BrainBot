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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Labubu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders.start()

    def cog_unload(self):
        self.reminders.cancel()
    @tasks.loop(minutes=1)
    async def reminders(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # use new mode if possible
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        )

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        url = "https://www.popmart.com/ca/pop-now/set/292"
        in_stock_xpath = "//button[span[text()='Pick One to Shake']]"

        try:
            driver.get(url)

            try:
                WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "//button[span[text()='Pick One to Shake']]")))
                # Now take screenshot (this will be after JS has rendered)
                # success = driver.save_screenshot("/tmp/debug_after_render.png")
                # print("Screenshot saved:", success)

                channel = self.bot.get_channel(1387286472029241354)
                embed = discord.Embed(description="🟢 **Restock Alert!** The item is now available.")
                await channel.send(embed=embed)

            except Exception as e:
                now = datetime.datetime.now()
                formatted_time = now.strftime("%Y-%m-%d %I:%M %p")
                channel = self.bot.get_channel(1387199146762703042)
                embed = discord.Embed(description=f"[{formatted_time}] Still OUT OF STOCK.")
                await channel.send(embed=embed)

        except Exception as e:
            print("❌ Page load or check failed:", e)

        finally:
            driver.quit()
    @reminders.before_loop
    async def before_reminder(self):
        print(f'Starting up Popmart alerts')
        await self.bot.wait_until_ready()
def setup(bot):
    bot.add_cog(Labubu(bot))