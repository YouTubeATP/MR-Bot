import discord
import os
import sys
import io
import traceback
from decouple import config
from discord.ext import commands
from discord.utils import get
import difflib
from disputils import BotEmbedPaginator

global prefix
prefix = 'm!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.remove_command('help')

token = config("TOKEN")
owner = config("OWNER")
botid = config("ID")

global botdev
botdev = str(owner)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="MR"))
    print('We have logged in as {0.user}. Bot is ready.'.format(bot))
    global aliases
    aliases = []
    for command in bot.commands:
        aliases += (list(command.aliases) + [command.name])
    
@bot.event
async def on_member_join(member, guild):
    if guild.id != 832673545090891808:
        return
    emojis = bot.get_guild(848231259440414750).emojis
    embed = discord.Embed(title=f"{get(emojis, name='join')} Member Joined", description=f"歡迎 <@{member.id}> 來到伺服器！\nWelcome <@{member.id}> to the server!", color=0x36393f)
    channel = bot.get_channel(832673546139729979)
    await channel.send(embed=embed)
    
@bot.event
async def on_member_remove(member, guild):
    if guild.id != 832673545090891808:
        return
    emojis = bot.get_guild(848231259440414750).emojis
    embed = discord.Embed(title=f"{get(emojis, name='leave')} Member Left", description=f"<@{member.id}> 離開了伺服器！下次再見\n<@{member.id}> has left the server! See you next time!", color=0x36393f)
    channel = bot.get_channel(832673546139729979)
    await channel.send(embed=embed)

## Message edit detection
@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)
    
@bot.event
async def on_command_error(ctx, error):
    triedCommand = ctx.message.content.split(" ")[0][2:]
    a = 1
    # If user added a space between prefix and command
    while len(triedCommand) == 0:
        triedCommand = ctx.message.content.split(" ")[a]
        a += 1
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        emojis = bot.get_guild(848231259440414750).emojis
        try:
            closest = difflib.get_close_matches(triedCommand, aliases)[0]
            embed = discord.Embed(title=f"{get(emojis, name='error')} 無效指令 Invalid Command", description=f"無效指令！您是指 `m!{closest}` 嗎？\nInvalid command! Did you mean `m!{closest}`?", color=0x36393f)
            await ctx.channel.send(embed=embed)
        except IndexError:
            embed = discord.Embed(title=f"{get(emojis, name='error')} 無效指令 Invalid Command", description=f"無效指令！\nInvalid command!", color=0x36393f)
            await ctx.channel.send(embed=embed)

@bot.command()
async def extload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

@bot.command()
async def extunload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

@bot.command()
async def extreload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded extension `{cog}`!')
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

@bot.command()
async def extlist(ctx):
    if str(ctx.author.id) == str(owner):
        exts = []
        for i in os.listdir('./cogs'):
            if i.endswith('.py'):
                exts.append(i[:-3])
        message1 = ''
        for j in exts:
            message1 += f'''`{j}`\n'''
        await ctx.send(message1)
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)
    
@bot.command(name='exec')
async def exec_command(ctx, *, arg1):
    if str(ctx.author.id) == botdev:
        arg1 = arg1[6:-4]
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            exec(arg1)
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
        except:
            x = traceback.format_exc()
            embed=discord.Embed(title=f'Execution Failed!', color=0xff0000)
            embed.set_author(name="MR Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed = embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="MR Bot")
            embed.add_field(name="Code", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

@bot.command(name='asyncDef')
async def asyncDef_command(ctx, *, arg1):
    if str(ctx.author.id) == botdev:
        arg1 = arg1[6:-4]
        try:
            func = "global asyncExec\nasync def asyncExec():\n"
            ## Indent each line of arg1 by 4 spaces
            for line in iter(arg1.splitlines()):
                func += "    " + line + "\n"
            exec(func)
        except:
            x = traceback.format_exc()
            embed=discord.Embed(title=f'Definition Failed!', color=0xff0000)
            embed.set_author(name="MR Bot")
            embed.add_field(name="Input", value=f'```py\n{str(arg1)}\n```', inline=False)
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'Definition Success!', color=0x00ff00)
            embed.set_author(name="MR Bot")
            embed.add_field(name="Function Definition", value=f'```py\n{str(func)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

@bot.command(name='asyncExec')
async def asyncExec_command(ctx):
    if str(ctx.author.id) == botdev:
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        try:
            global asyncExec
            await asyncExec()
            output = new_stdout.getvalue()
            sys.stdout = old_stdout
            del asyncExec
        except:
            x = traceback.format_exc()
            embed=discord.Embed(title=f'Execution Failed!', color=0xff0000)
            embed.set_author(name="MR Bot")
            embed.add_field(name="Output", value=f'```\n{str(x)}\n```', inline=False)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f'Execution Success!', color=0x00ff00)
            embed.set_author(name="MR Bot")
            embed.add_field(name="Output", value=f'```\n{str(output)}\n```', inline=False)
            await ctx.send(embed=embed)
    else:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    emojis = bot.get_guild(848231259440414750).emojis
    embed = discord.Embed(title=f"{get(emojis, name='ping')} 延遲 Ping", description=f"**{round(bot.latency * 1000)}ms**", color=0x36393f)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    emojis = bot.get_guild(848231259440414750).emojis
    embed1=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="help")} `m!help`
{get(emojis, name='space')} 此指令。
{get(emojis, name='space')} This command.""", color=0x36393f)
    embed2=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="ping")} `m!ping`
{get(emojis, name='space')} 獲得機器人的延遲。 
{get(emojis, name='space')} Returns the latency in ms.""", color=0x36393f)
    embed3=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="usernamereg")} `m!usernamereg [java|bedrock] [username]`
{get(emojis, name='space')} 註冊您的 Minecraft 使用者名稱。
{get(emojis, name='space')} Register your Minecraft username.""", color=0x36393f)
    embed4=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="username")} `m!username [java|bedrock] [mentionuser]`
{get(emojis, name='space')} 查詢一個 Discord 用戶的 Minecraft 使用者名稱。 
{get(emojis, name='space')} Query a Minecraft username of a Discord user.""", color=0x36393f)
    embed5=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="data")} m!data {{車站代號 Station Code}} {{eng|chi}}
{get(emojis, name='space')} 取得一個 MR 車站的資訊。 
{get(emojis, name='space')} Obtain data of an MR station.""", color=0x36393f)
    embed1.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed2.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed3.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed4.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed5.set_footer(text="[] 必填 Required {} 選填 Optional")
    embeds = [embed1, embed2, embed3, embed4, embed5]
    paginator = BotEmbedPaginator(ctx, embeds)
    await paginator.run()

@bot.command()
async def send(ctx, *, content):
    if ctx.author.id != 438298127225847810:
        emojis = bot.get_guild(848231259440414750).emojis
        embed = discord.Embed(title=f"{get(emojis, name='error')} 無權限 No Permission", description="抱歉。您沒有足夠權限執行此操作。\nSorry, but you don't have permission to do that.", color=0x36393f)
        await ctx.send(embed=embed)
        return
    await ctx.send(content)
    
### SLASH COMMANDS ZONE ###

from discord_slash import SlashCommand
slash = SlashCommand(bot, sync_commands=True, override_type=True)

guildID = 832673545090891808

@slash.slash(name="ping", 
             description="獲得機器人的延遲 Returns the latency in ms",
             guild_ids=[guildID])
async def _ping(ctx):
    emojis = bot.get_guild(848231259440414750).emojis
    embed = discord.Embed(title=f"{get(emojis, name='ping')} 延遲 Ping", description=f"**{round(bot.latency * 1000)}ms**", color=0x36393f)
    await ctx.send(embed=embed)
    
@slash.slash(name="help",
             description="獲得機器人的使用指南 Returns the user guide of this bot",
             guild_ids=[guildID])
async def help(ctx):
    emojis = bot.get_guild(848231259440414750).emojis
    embed1=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="help")} `/help`
{get(emojis, name='space')} 此指令。
{get(emojis, name='space')} This command.""", color=0x36393f)
    embed2=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="ping")} `/ping`
{get(emojis, name='space')} 獲得機器人的延遲。 
{get(emojis, name='space')} Returns the latency in ms.""", color=0x36393f)
    embed3=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="usernamereg")} `/usernamereg [java|bedrock] [username]`
{get(emojis, name='space')} 註冊您的 Minecraft 使用者名稱。
{get(emojis, name='space')} Register your Minecraft username.""", color=0x36393f)
    embed4=discord.Embed(title=f"{get(emojis, name='help')} MR Bot 使用指南 User Guide", description=f"""{get(emojis, name="username")} `/username [java|bedrock] [mentionuser]`
{get(emojis, name='space')} 查詢一個 Discord 用戶的 Minecraft 使用者名稱。 
{get(emojis, name='space')} Query a Minecraft username of a Discord user.""", color=0x36393f)
    embed1.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed2.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed3.set_footer(text="[] 必填 Required {} 選填 Optional")
    embed4.set_footer(text="[] 必填 Required {} 選填 Optional")
    embeds = [embed1, embed2, embed3, embed4]
    paginator = BotEmbedPaginator(ctx, embeds)
    embed = discord.Embed(title=f"{get(emojis, name='error')} 留意下面訊息 Refer below", description="使用指南在下面訊息內。\nRefer to the message below for the help menu.", color=0x36393f)
    await ctx.send(embed=embed)
    await paginator.run()

def runBot():    
    for i in os.listdir('./cogs'):
        if i.endswith('.py'):
            bot.load_extension(f'cogs.{i[:-3]}')
    print('Extensions loaded!')
    bot.run(token)
    
runBot()