import requests
import discord
from discord.ext import commands, tasks
from discord.commands import slash_command
from discord.ui import View, Button
import requests
import warnings
import base64
    
invitationId = 0
with open("/Applications/League of Legends.app/Contents/LoL/lockfile") as r:
        lockfile = r.read().split(':')
headers = {"Authorization" : "Basic " + str(base64.b64encode(bytes('riot:' + lockfile[3], 'utf-8')))[2:-1]}
def request(method, endpoint, data=None):
    return requests.request(method, "https://127.0.0.1:" + lockfile[2] + endpoint, verify = False, headers=headers, json=data)

class Invites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.myLoop.start()
    @tasks.loop(seconds = 10) # repeat after every 10 seconds
    async def myLoop(self):
        async def button_callback(interaction):
            await interaction.response.send_message("Accepted", ephemeral=True)
            invitations = request("GET", "/lol-lobby/v2/received-invitations")
            request("POST", "/lol-lobby/v2/received-invitations/"+ invitations.json()[0]["invitationId"] +"/accept")
        warnings.filterwarnings("ignore")
        try:
            invitations = request("GET", "/lol-lobby/v2/received-invitations")
            if(invitations.json() != []):
                print("You have been invited to a game")
                accept_button = Button(label="Accept", style=discord.ButtonStyle.green)
                accept_button.callback = button_callback
                view = View()
                view.add_item(accept_button)
                channel = self.bot.get_channel(1065813803150880800)
                await channel.send("You have been invited to a game by " + invitations.json()[0]["fromSummonerName"] + "!", view=view)
        except Exception as e:
            print(e)
            pass
    @myLoop.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()
    @slash_command(name='accept', description="Accepts the first invite", guild_ids=[1065813802425262141])
    async def accept(self, ctx):
        try:
            invitations = request("GET", "/lol-lobby/v2/received-invitations")
            request("POST", "/lol-lobby/v2/received-invitations/"+ invitations.json()[0]["invitationId"] +"/accept")
            await ctx.respond("Accepted")
        except:
            await ctx.respond("No invites")
def setup(bot):
    bot.add_cog(Invites(bot))