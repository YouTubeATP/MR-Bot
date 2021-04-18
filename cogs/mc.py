import discord
from discord.ext import commands
import boto3
import json
from decouple import config
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

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
                if version in usernames[str(ctx.author.id)]:
                    usernames[str(ctx.author.id)] = username
                else:
                    usernames.update({f"{str(ctx.author.id)}": f"{username}"})
            else:
                usernames.update({f"{str(ctx.author.id)}": f"{username}"})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            with open("usernames.json", "rb") as f:
                client.upload_fileobj(f, "mr-bot", "usernames.json")
            await ctx.send(f"<@{ctx.author.id}>，已註冊您的使用者名稱 **{username}**。\nRegistered your username as **{username}**, <@{ctx.author.id}>.")
        else:
            await ctx.send("請輸入一個使用者名稱！ Please input a username!")

    @commands.command(name="username")
    async def un(self, ctx, *, user: discord.User):
        usernames = json.loads(client.get_object(Bucket="mr-bot", Key="usernames.json")["Body"].read())
        try:
            await ctx.send(f"Discord 用戶 **{user.name}#{user.discriminator}** 的使用者名稱是\n**__{usernames[str(user.id)]}__**\n\nThe username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)]}__**")
        except KeyError:
            await ctx.send("該用戶尚未註冊使用者名稱。 That user hasn't registered their username yet!")
            
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
                if version in usernames[str(ctx.author.id)]:
                    usernames[str(ctx.author.id)] = username
                else:
                    usernames.update({f"{str(ctx.author.id)}": f"{username}"})
            else:
                usernames.update({f"{str(ctx.author.id)}": f"{username}"})
            with open("usernames.json", "w") as f:
                json.dump(usernames, f, indent=4)
            with open("usernames.json", "rb") as f:
                client.upload_fileobj(f, "mr-bot", "usernames.json")
            await ctx.send(f"<@{ctx.author.id}>，已註冊您的使用者名稱 **{username}**。\nRegistered your username as **{username}**, <@{ctx.author.id}>.")
        else:
            await ctx.send("請輸入一個使用者名稱！ Please input a username!")
            
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
            await ctx.send(f"Discord 用戶 **{user.name}#{user.discriminator}** 的使用者名稱是\n**__{usernames[str(user.id)]}__**\n\nThe username of Discord user **{user.name}#{user.discriminator}** is:\n**__{usernames[str(user.id)]}__**")
        except KeyError:
            await ctx.send("該用戶尚未註冊使用者名稱。 That user hasn't registered their username yet!")

def setup(bot):
    bot.add_cog(Minecraft(bot))
