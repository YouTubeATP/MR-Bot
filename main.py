import discord
import os
import sys
import io
import traceback
import yaml
from decouple import config
from discord.ext import commands
import difflib

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
        try:
            closest = difflib.get_close_matches(triedCommand, aliases)[0]
            await ctx.channel.send(f"無效指令！您是指 `m!{closest}` 嗎？ Invalid command! Did you mean `m!{closest}`?")
        except IndexError:
            await ctx.channel.send("無效指令！ Invalid command!")

@bot.command()
async def extload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Loaded extension `{cog}`!')
    else:
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")

@bot.command()
async def extunload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        await ctx.send(f'Unloaded extension `{cog}`!')
    else:
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")

@bot.command()
async def extreload(ctx, cog):
    if str(ctx.author.id) == str(owner):
        bot.unload_extension(f'cogs.{cog}')
        bot.load_extension(f'cogs.{cog}')
        await ctx.send(f'Reloaded extension `{cog}`!')
    else:
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")

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
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")
    
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
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")

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
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")

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
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you don't have permission to do that.")

@bot.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: **{round(bot.latency * 1000)}ms**')

@bot.command()
async def help(ctx):
    await ctx.send("""***MR Bot 使用指南 User Guide***
`m!ping`
獲得機器人的延遲。 Returns the latency in ms.

`m!help`
此指令。 This command.

`m!data {車站代號 Station Code} {eng|chi}`
取得一個 MR 車站的資訊。 Obtain data of an MR station.

[] 必填 Required
{} 選填 Optional""")

@bot.command()
async def send(ctx, *, content):
    if ctx.author.id != 438298127225847810:
        await ctx.send("抱歉。您沒有足夠權限執行此操作。 Sorry, but you do not have permission to do that.")
        return
    await ctx.send(content)

def runBot():    
    for i in os.listdir('./cogs'):
        if i.endswith('.py'):
            bot.load_extension(f'cogs.{i[:-3]}')
    print('Extensions loaded!')
    bot.run(token)
    
runBot()