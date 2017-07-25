import discord
from ext.commands import Bot
from ext import commands
import datetime
import time
import sys
import asyncio
from cogs.utils import launcher
import json
import logging
import random


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


##launcher.check()
 

info = launcher.bot()
token = info['token']
owner = info['owner']



startup_extensions = [

    'cogs.info',
    'cogs.misc',
    'cogs.mod',
    'cogs.embed',
    'cogs.tourney',
    'cogs.polls',
    'cogs.robolog',
    'cogs.tags',
    'cogs.setup',
    'cogs.levels',
    'cogs.clashroyale',
    'cogs.repl',
    'cogs.alias'
]

Client = discord.Client()
description = ('A rogue Knight stumbled upon discord. '
'Made by verix \n')


async def get_pre(bot, message):
    with open('cogs/utils/t_config.json') as f:
        config = json.loads(f.read())
    try:
        if message.server.id not in config:
            return '.'
    except:
        pass
    else:
        return config[message.server.id]['prefix']

bot = commands.Bot(description=description, command_prefix=get_pre, pm_help=None)

@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: verix')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    bot.uptime = datetime.datetime.now()



def owner_only():
    return commands.check(lambda ctx: ctx.message.author == ctx.message.server.owner)

def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)


@bot.event
async def on_member_join(member):
    with open('cogs/utils/t_config.json') as f:
        data = json.loads(f.read())
    server = member.server
    status = data[server.id]["welcome"]["status"]
    if status:
        fmt = data[server.id]["welcome"]["msg"]
        channel = data[server.id]["welcome"]["channel"]
        if channel == 'default':
            channel = member.server
        else:
            channel = discord.utils.get(server.channels, id=channel)

        await bot.send_message(channel, fmt.format(member, server))

    autorole = data[server.id]["autorole"]
    autorole = discord.utils.get(server.roles,id=autorole)

    try:
        await bot.add_roles(member,autorole)
    except:
        pass

@bot.event
async def on_command(command, ctx):
    print('------------------------------------')
    print('Command > {}{} < invoked with > {} <\nServer: {} | {}\nUser: {} | {}'
        .format(ctx.prefix,
            command,
            ctx.invoked_with,
            ctx.message.server.name, 
            ctx.message.server.id, 
            ctx.message.author.name, 
            ctx.message.author.id))

@bot.event
async def on_member_remove(member):
    server = member.server
    with open('cogs/utils/t_config.json') as f:
        data = json.loads(f.read())
    status = data[server.id]["leave"]["status"]
    if status:
        msg = data[server.id]["leave"]["msg"]
        channel = data[server.id]['leave']['channel']
        if channel == 'default':
            channel = server
        else:
            channel = discord.utils.get(server.channels, id=channel)

        await bot.send_message(channel, msg.format(member, server))

@bot.event
async def on_server_join(server):
    await bot.send_message(server,
        "**Hello!** *Thanks for inviting me to your server!*"
        " **Get started with:** `.config set` and `.help`")


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
        print('Sent command help')
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
        print('Sent command help')

@bot.event
async def on_command_error(error, ctx):
   print(error)
   channel = ctx.message.channel
   if isinstance(error, commands.MissingRequiredArgument):
       await send_cmd_help(ctx)
       print('Sent command help')
   elif isinstance(error, commands.BadArgument):
       await send_cmd_help(ctx)
       print('Sent command help')
   elif isinstance(error, commands.DisabledCommand):
       await bot.send_message(channel, "That command is disabled.")
       print('Command disabled.')
   elif isinstance(error, commands.CommandInvokeError):
       # A bit hacky, couldn't find a better way
       no_dms = "Cannot send messages to this user"
       is_help_cmd = ctx.command.qualified_name == "help"
       is_forbidden = isinstance(error.original, discord.Forbidden)
       if is_help_cmd and is_forbidden and error.original.text == no_dms:
           msg = ("I couldn't send the help message to you in DM. Either"
                  " you blocked me or you disabled DMs in this server.")
           await bot.send_message(channel, msg)
           return

@bot.command(pass_context=True,name='cog')
@owner_only()
async def _reload(ctx,*, module : str):
    """Reloads a module."""
    channel = ctx.message.channel
    module = 'cogs.'+module
    try:
        bot.unload_extension(module)
        x = await bot.send_message(channel,'Successfully Unloaded.')
        bot.load_extension(module)
        x = await bot.edit_message(x,'Successfully Reloaded.')
    except Exception as e:
        x = await bot.edit_message(x,'\N{PISTOL}')
        await bot.say('{}: {}'.format(type(e).__name__, e))
    else:
        x = await bot.edit_message(x,'Done. \N{OK HAND SIGN}')

@bot.command(name='presence',hidden=True)
@is_owner()
async def _set(Type=None,*,thing=None):
        if Type is None:
                await bot.say('Usage: `.presence [game/stream] [message]`')
        else:
                if Type.lower() == 'stream':
                        await bot.change_presence(game=discord.Game(
                            name=thing,type=1,url='https://www.twitch.tv/a'),status='online')
                        await bot.say('Done.')
                elif Type.lower() == 'game':
                        await bot.change_presence(game=discord.Game(name=thing))
                        await bot.say('Done.')
                elif Type.lower() == 'clear':
                        await bot.change_presence(game=None)
                        await bot.say('Done.')
                else:
                        await bot.say('Usage: `.presence [game/stream] [message]`')

@bot.command(pass_context=True)
@is_owner()
async def _leave_all_servers_(ctx):
    for server in bot.servers:
        await bot.leave_server(server)
        await bot.say('I left `{}`'.format(server.name))

@bot.command(pass_context=True)
async def servers(ctx):
    servers = ', '.join([i.name for i in bot.servers]).strip(', ')
    await bot.say('**Current list of servers:**\n ```bf\n{}```'.format(servers))



if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded extension: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(token)
