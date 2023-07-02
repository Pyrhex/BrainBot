import discord
from discord.ext import commands
from discord.commands import slash_command
from gpt4free import you
from brainbot import guildList

class GPT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @slash_command(name='askgpt', description='Interact with ChatGPT', guild_ids=guildList)
    async def askgpt(self, ctx, prompt):
        await ctx.defer()
        try:
            response = you.Completion.create(
                prompt=prompt,
                detailed=True,
                include_links=True, )
            embed=discord.Embed(description=response.text, color=0x141414)
            await ctx.respond(embed=embed)
        except Exception as e:
            embed=discord.Embed(description=f"Error: {e}", color=0x141414)
            await ctx.respond(embed=embed)
            


def setup(bot):
    bot.add_cog(GPT(bot))
