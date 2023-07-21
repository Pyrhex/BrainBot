import discord
import re
from discord.ext import commands
import requests
import os

def getDict() -> dict:
    response = requests.get('https://ttdownloader.com/')
    point = response.text.find('<input type="hidden" id="token" name="token" value="') + \
        len('<input type="hidden" id="token" name="token" value="')
    token = response.text[point:point+64]
    TTDict = {
        'token': token,
    }

    for i in response.cookies:
        TTDict[str(i).split()[1].split('=')[0].strip()] = str(
            i).split()[1].split('=')[1].strip()
    return TTDict

def createHeader(parseDict) -> list:

    cookies = {
        'PHPSESSID': parseDict['PHPSESSID'],
        # 'popCookie': parseDict['popCookie'],
    }
    headers = {
        'authority': 'ttdownloader.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://ttdownloader.com',
        'referer': 'https://ttdownloader.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
    data = {
        'url': '',
        'format': '',
        'token': parseDict['token'],
    }
    return cookies, headers, data


def TDL(link, name) -> None:
    parseDict = getDict()
    cookies, headers, data = createHeader(parseDict)
    data['url'] = link
    response = requests.post('https://ttdownloader.com/search/',
                             cookies=cookies, headers=headers, data=data)
    linkParse = [i for i in str(response.text).split()
                 if i.startswith("href=")][0]
    response = requests.get(linkParse[6:-10])
    # print(response.content)
    with open("./vids/"+name+".mp4", "wb") as f:
        f.write(response.content)

class Tiktok(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if(message.author.bot):
            return
        if(".tiktok." in message.content):
            link = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
            print(link)
            if("||" in message.content):
                filename = f'SPOILER_{message.id}'
            else:
                filename = f'{message.id}'
            await message.edit(suppress=True)
            TDL(link, filename)
            await message.reply(file=discord.File(os.path.realpath(os.path.join(os.path.dirname(__file__), '../vids',filename)) + ".mp4"))
            file_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../vids',filename)) + ".mp4"
            os.remove(file_path)
            print("done")
            
def setup(bot):
    bot.add_cog(Tiktok(bot))
