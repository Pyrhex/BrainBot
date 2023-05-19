import os
import yt_dlp as youtube_dl
import discord
from discord.ext import commands
from discord.commands import slash_command
from brainbot import guildList

class YoutubeMP3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name='convert', description="Converts the Youtube video into an MP3 file", guild_ids=guildList)
    async def convert(self, ctx, video_url: str):
        await ctx.defer()
        try:
            video_info = youtube_dl.YoutubeDL().extract_info(
                url = video_url,download=False
            )
            filename = video_info['title']
            options = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': filename,
                "quiet": True
            }
            file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..',filename)) + ".mp3"

            with youtube_dl.YoutubeDL(options) as ydl:
                ydl.download([video_info['webpage_url']])
            file = discord.File(file_path)
            await ctx.channel.send(file=file)
            await ctx.respond("Download complete... {}".format(filename))
            os.remove(file_path)
        except Exception as e:
            await ctx.respond(e)


def setup(bot):
    bot.add_cog(YoutubeMP3(bot))