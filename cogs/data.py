import discord
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def data(self, ctx, stationCode=None, lang=None):
        emojis = self.bot.get_guild(848231259440414750).emojis
        with open("assets/stationData.xml", "r", encoding="utf8") as f:
            bsData = BeautifulSoup(f.read(), "lxml") 
        if not stationCode:
            res = ""
            for station in bsData.find_all("station"):
                lines = station.find("line").string.split(" ")
                stationType = "checkpoint" if len(lines) >= 3 else "station"
                if stationType == "checkpoint":
                    res += f"""`{station.get("code")}` - {station.find("cname").string}檢查站 {station.find("ename").string} Checkpoint\n"""
                else:
                    res += f"""`{station.get("code")}` - {station.find("cname").string}站 {station.find("ename").string} Station\n"""
            embed = discord.Embed(title=f"{get(emojis, name='error')} 輸入一個車站代號 Input a station code", description=res, color=0x36393f)
            await ctx.send(embed=embed)
            return
        if not lang:
            lang = "chi"
        station = bsData.find("station", {"code": stationCode})
        if not station:
            embed = discord.Embed(title=f"{get(emojis, name='error')} 參數錯誤 Argument Error", description="參數無效！\nArgument is invalid!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        lines = station.find("line").string.split(" ")
        exits = int(station.find("exit").string)
        if lang == "eng":
            name = station.find("ename").string
            stationType = "Checkpoint" if len(lines) >= 3 else "Station"
            lineNames = {"MSL": "Milestone Line", "NEL": "New Era Line", "EWL": "East-West Line", "CAL": "Cave Line", "CIL": "City Line", "EBL": "EST Branch Line", "IIL": "Interisland Line"}
        elif lang == "chi":    
            name = station.find("cname").string
            stationType = "檢查站" if len(lines) >= 3 else "站"
            lineNames = {"MSL": "里程綫", "NEL": "新代綫", "EWL": "東西綫", "CAL": "洞穴綫", "CIL": "城市綫", "EBL": "站站講支綫", "IIL": "群島綫"}
        else:
            await ctx.send("參數無效！ Invalid argument!")
            return
        linee = ""
        if lang == "eng":
            embed=discord.Embed(title=f"{get(emojis, name='data')} {name} {stationType}", color=0x36393f)
            for line in lines:
                linee += lineNames[line] + ", "
            embed.add_field(name=f"{get(emojis, name='lines')}  Passing Lines", value=linee[:-2], inline=True)
            embed.add_field(name=f"{get(emojis, name='exit')}  No. of exits", value=exits, inline=True)
        elif lang == "chi":
            embed=discord.Embed(title=f"{get(emojis, name='data')} {name}{stationType}", color=0x36393f)
            for line in lines:
                linee += lineNames[line] + "、"
            embed.add_field(name=f"{get(emojis, name='lines')}  途經路綫", value=linee[:-1], inline=True)
            embed.add_field(name=f"{get(emojis, name='exit')}  出口數量", value=exits, inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Data(bot))
