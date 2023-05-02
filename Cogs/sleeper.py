import requests
import discord
from discord.ext import commands
from discord.commands import slash_command
from sleeperpy import Leagues
from discord.ui import View, Button
league_id = 911894191154827264
players = requests.get("https://api.sleeper.app/v1/players/lcs")
users = Leagues.get_users(league_id)
rosters = Leagues.get_rosters(league_id)
matchups = Leagues.get_matchups(league_id, 1)
def ownerIdToName(owner_id):
    for i in users:
        if(i["user_id"] == owner_id):
            return i["display_name"]

def getUser(roster_id):
    for i in rosters:
        if(i["roster_id"] == roster_id):
            return i["owner_id"]
def getPlayerName(id):
    return players.json()[str(id)]["metadata"]["username"]
def sortByRole(player_points):
    new_dict = []
    new_dict.append(sorted(player_points.items(), key=lambda x: players.json()[x[0]]["position"])[4])
    new_dict.append(sorted(player_points.items(), key=lambda x: players.json()[x[0]]["position"])[1])    
    new_dict.append(sorted(player_points.items(), key=lambda x: players.json()[x[0]]["position"])[2])    
    new_dict.append(sorted(player_points.items(), key=lambda x: players.json()[x[0]]["position"])[0])    
    new_dict.append(sorted(player_points.items(), key=lambda x: players.json()[x[0]]["position"])[3])    
    return dict(new_dict)

def reformatPlayerPoints(player_points):
    player_points = sortByRole(player_points)
    new_player_points = dict((getPlayerName(k), v) for k, v in player_points.items())
    return new_player_points

def getCurrScore(username):
    for i in matchups:
        if(ownerIdToName(getUser(i["roster_id"])) == username):
            return reformatPlayerPoints(i["players_points"])
def getMatchup(username, matchups):
    for i in matchups:
        if(ownerIdToName(getUser(i["roster_id"])) == username):
            matchup_id = i["matchup_id"]
    for i in matchups:
        if(matchup_id == i["matchup_id"] and ownerIdToName(getUser(i["roster_id"])) != username):
            return reformatPlayerPoints(i["players_points"])

class Sleeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @slash_command(name='matchup', description="Turns Brian's light green", guild_ids=[1065813802425262141])
    async def matchup(self, ctx, username):
        button = Button(label="Refresh", style=discord.ButtonStyle.green)
        async def button_callback(interaction):
            new_matchups = Leagues.get_matchups(league_id, 1)
            new_embed = discord.Embed(title="Matchup", description="This is a matchup")
            for k,v in getMatchup(username, new_matchups).items():     
                new_embed.add_field(name=k, value=v, inline=False)   
            await interaction.response.edit_message(embed=new_embed, view=view)
        button.callback = button_callback
        view = View()
        view.add_item(button)
        embed = discord.Embed(title="Matchup", description="This is a matchup")
        for k,v in getMatchup(username, matchups).items():     
            embed.add_field(name=k, value=v, inline=False)       
        something = await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Sleeper(bot))