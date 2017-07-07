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
logger.setLevel(logging.DEBUG)
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
    'cogs.levels'
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
    print('------------------------------------')






def owner_only():
    return commands.check(lambda ctx: ctx.message.author == ctx.message.server.owner)

def is_owner():
    return commands.check(lambda ctx: ctx.message.author.id == owner)


@bot.event
async def on_member_join(member):
    server = member.server
    role = 'Larry'
    fmt = 'Welcome {0.mention} to {1.name}!'
    autorole = discord.utils.get(server.roles,name=role)
    await bot.send_message(server, fmt.format(member, server))
    await bot.add_roles(member,autorole)

@bot.event
async def on_member_remove(member):
    server = member.server
    fmt = '{0.name} has just left the server.'.format(member)
    await bot.send_message(server, fmt)


async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)
    else:
        pages = bot.formatter.format_help_for(ctx, ctx.command)
        for page in pages:
            await bot.send_message(ctx.message.channel, page)

@bot.event
async def on_command_error(error, ctx):
 channel = ctx.message.channel
 if isinstance(error, commands.MissingRequiredArgument):
     await send_cmd_help(ctx)
 elif isinstance(error, commands.BadArgument):
     await send_cmd_help(ctx)
 elif isinstance(error, commands.DisabledCommand):
     await bot.send_message(channel, "That command is disabled.")
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
            print('Succesfully loaded extenstion: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))


bot.run(token)
