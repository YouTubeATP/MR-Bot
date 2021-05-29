import discord
from discord.ext import commands
from discord.utils import get
import boto3
import json
from decouple import config
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option


## AWS setup
key = config("AWSKEY") # AWS Access Key ID
secret = config("AWSSECRET") # AWS Secret Access Key
client = boto3.client("s3", aws_access_key_id=key, aws_secret_access_key=secret) # Initialize boto3 client

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="usernamereg")
    async def unr(self, ctx, *, username=None):
        if username:
            usernames = json.loads(client.get_object(Bucket="mr-bot", Key="usernames.json")["Body"].read())
            ## Checking which entries exist
            if f"{str(ctx.author.id)}" in usernames:
                usernames[str(ctx.author.id)] = username
            else:
                usernames.update({f"{str(ctx.author.id)}": f"{username}"})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            with open("usernames.json", "rb") as f:
                client.upload_fileobj(f, "mr-bot", "usernames.json")
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='success')} 註冊成功 Registration Successful", description=f"<@{ctx.author.id}>，已註冊您的使用者名稱 **{username}**。\nRegistered your username as **{username}**, <@{ctx.author.id}>.", color=0x36393f)
            await ctx.send(embed=embed)
        else:
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} 參數錯誤 Argument Error", description="請輸入一個使用者名稱！\nPlease input a username!", color=0x36393f)
            await ctx.send(embed=embed)

    @commands.command(name="username")
    async def un(self, ctx, *, user: discord.User):
        usernames = json.loads(client.get_object(Bucket="mr-bot", Key="usernames.json")["Body"].read())
        try:
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='username')} Minecraft 使用者名稱查詢 Minecraft Username Query", description=f"Discord 用戶 **{user.name}#{user.discriminator}** 的使用者名稱是\n**__{usernames[str(user.id)]}__**\n\nThe username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)]}__**", color=0x36393f)
            await ctx.send(embed=embed)
        except KeyError:
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} 用戶名稱未註冊 Username Not Registered", description="該用戶尚未註冊使用者名稱。\nThat user hasn't registered their username yet!", color=0x36393f)
            await ctx.send(embed=embed)
            
    ### SLASH COMMANDS ZONE ###
    
    guildID = 832673545090891808
    
    @cog_ext.cog_slash(name="usernamereg",
                       description="註冊您的 Minecraft 使用者名稱 Register your Minecraft username",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="username",
                               description="Minecraft 使用者名稱 Minecraft username",
                               option_type=3,
                               required=True
                           )
                       ])
    async def _unr(self, ctx: SlashContext, *, username=None):
        if username:
            await ctx.defer()
            usernames = json.loads(client.get_object(Bucket="mr-bot", Key="usernames.json")["Body"].read())
            ## Checking which entries exist
            if f"{str(ctx.author.id)}" in usernames:
                usernames[str(ctx.author.id)] = username
            else:
                usernames.update({f"{str(ctx.author.id)}": f"{username}"})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            with open("usernames.json", "rb") as f:
                client.upload_fileobj(f, "mr-bot", "usernames.json")
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='success')} 註冊成功 Registration Successful", description=f"<@{ctx.author.id}>，已註冊您的使用者名稱 **{username}**。\nRegistered your username as **{username}**, <@{ctx.author.id}>.", color=0x36393f)
            await ctx.send(embed=embed)
        else:
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} 參數錯誤 Argument Error", description="請輸入一個使用者名稱！\nPlease input a username!", color=0x36393f)
            await ctx.send(embed=embed)
            
    @cog_ext.cog_slash(name="username",
                       description="查詢一個 Discord 用戶的 Minecraft 使用者名稱 Query a Minecraft username of a Discord user",
                       guild_ids=[guildID],
                       options=[
                           create_option(
                               name="user",
                               description="查詢的 Discord 用戶 the Discord user you want to query",
                               option_type=6,
                               required=True
                           )
                       ])
    async def _un(self, ctx: SlashContext, *, user: discord.User):
        await ctx.defer()
        usernames = json.loads(client.get_object(Bucket="mr-bot", Key="usernames.json")["Body"].read())
        try:
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='username')} Minecraft 使用者名稱查詢 Minecraft Username Query", description=f"Discord 用戶 **{user.name}#{user.discriminator}** 的使用者名稱是\n**__{usernames[str(user.id)]}__**\n\nThe username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)]}__**", color=0x36393f)
            await ctx.send(embed=embed)
        except KeyError:
            emojis = self.bot.get_guild(848231259440414750).emojis
            embed = discord.Embed(title=f"{get(emojis, name='error')} 用戶名稱未註冊 Username Not Registered", description="該用戶尚未註冊使用者名稱。\nThat user hasn't registered their username yet!", color=0x36393f)
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Minecraft(bot))
