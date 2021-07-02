import discord
from discord.ext import commands
from discord.utils import get
from bs4 import BeautifulSoup
import math

class Distance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def distance(self, ctx, stationCode1=None, stationCode2=None, lang=None):
        emojis = self.bot.get_guild(848231259440414750).emojis
        with open("assets/stationData.xml", "r", encoding="utf8") as f:
            bsData = BeautifulSoup(f.read(), "lxml") 
        if not (stationCode1 and stationCode2):
            res = ""
            for station in bsData.find_all("station"):
                lines = station.find("line").string.split(" ")
                stationType = "checkpoint" if len(lines) >= 3 else "station"
                if stationType == "checkpoint":
                    res += f"""`{station.get("code")}` - {station.find("cname").string}檢查站 {station.find("ename").string} Checkpoint\n"""
                else:
                    res += f"""`{station.get("code")}` - {station.find("cname").string}站 {station.find("ename").string} Station\n"""
            embed = discord.Embed(title=f"{get(emojis, name='error')} 輸入兩個車站代號 Input two station codes", description=res, color=0x36393f)
            await ctx.send(embed=embed)
            return
        lang = "chi" if not lang else lang
        station1 = bsData.find("station", {"code": stationCode1})
        x1 = int(station1.find("x").string)
        z1 = int(station1.find("z").string)
        lines1 = station1.find("line").string.split(" ")
        station2 = bsData.find("station", {"code": stationCode2})
        x2 = int(station2.find("x").string)
        z2 = int(station2.find("z").string)
        lines2 = station2.find("line").string.split(" ")
        if not (station1 and station2):
            embed = discord.Embed(title=f"{get(emojis, name='error')} 參數錯誤 Argument Error", description="參數無效！\nArgument is invalid!", color=0x36393f)
            await ctx.send(embed=embed)
            return
        distance = math.sqrt((x2-x1)**2 + (z2-z1)**2)
        if lang == "eng":
            name1 = station1.find("ename").string
            stationType1 = "Checkpoint" if len(lines1) >= 3 else "Station"
            name2 = station2.find("ename").string
            stationType2 = "Checkpoint" if len(lines2) >= 3 else "Station"
        elif lang == "chi":    
            name1 = station1.find("cname").string
            stationType1 = "檢查站" if len(lines1) >= 3 else "站"
            name2 = station2.find("cname").string
            stationType2 = "檢查站" if len(lines2) >= 3 else "站"
        else:
            await ctx.send("參數無效！ Invalid argument!")
            return
        linee = ""
        if lang == "eng":
            embed=discord.Embed(title=f"{get(emojis, name='distance')} {name1} {stationType1} to {name2} {stationType2}", description=f"\u221a({(x2-x1)**2 + (z2-z1)**2}) blocks \u2248 {round(math.sqrt((x2-x1)**2 + (z2-z1)**2))} blocks", color=0x36393f)
        elif lang == "chi":
            embed=discord.Embed(title=f"{get(emojis, name='distance')} {name1}{stationType1} 至 {name2}{stationType2}", description=f"\u221a({(x2-x1)**2 + (z2-z1)**2})格 \u2248 {round(math.sqrt((x2-x1)**2 + (z2-z1)**2))}格", color=0x36393f)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Distance(bot))
