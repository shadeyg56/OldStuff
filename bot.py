import discord 
from ext.commands import Bot
from ext import commands
import datetime
import time
import sys
import asyncio
import os
from cogs.utils import launcher
import json
import logging
import random
from cogs.utils.paginator import Pages

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


##launcher.check()
 
if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']
 
info = launcher.bot()
owner = info['owner']



startup_extensions = [
 
 
    'cogs.mod',
    'cogs.old_misc'
 
 
]

Client = discord.Client()
description = ('Bot made with discord.py by -= shadeyg56 =-#1702. '
'Made by shadeyg56 \n')


async def get_pre(bot, message):
    with open('cogs/utils/t_config.json') as f:
        config = json.loads(f.read())
    try:
        if message.server.id not in config:
            return 'd.'
    except:
        pass
    else:
        return config[message.server.id]['prefix']

bot = commands.Bot(description=description, command_prefix=get_pre, pm_help=None)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('------------------------------------')
    print('THE BOT IS ONLINE')
    print('------------------------------------')
    print("Name: {}".format(bot.user.name))
    print('Author: shadeyg56')
    print("ID: {}".format(bot.user.id))
    print('DV: {}'.format(discord.__version__))
    bot.uptime = datetime.datetime.now()
    server = len(bot.servers)
    while 1 == 1:
        await bot.change_presence(game=discord.Game(name='with {} servers'.format(server)))
        await asyncio.sleep(10)
        await bot.change_presence(game=discord.Game(name='PREFIX = d.'))
        await asyncio.sleep(10)
        await bot.change_presence(game=discord.Game(name='Currently WIP | Darkness'))
        await asyncio.sleep(10)
                            
    


@bot.command(pass_context=True)
async def help(ctx):
    await bot.delete_message(ctx.message)

    msg = open('cogs/utils/help.txt').read().replace('\\u200b','\u200b').splitlines()
    for i, line in enumerate(msg): 
        if line.strip().startswith('.'):
            x = line.strip().strip('.')
            x = ctx.prefix + x
            msg[i] = '`' + x + '`'

    p = Pages(bot, message=ctx.message, entries=msg)
    p.embed.set_author(name='Help - Darkness Commands', icon_url=bot.user.avatar_url)
    p.embed.color = 0x00FFFF
    await p.paginate()

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
        if fmt == 'random_msg':
            with open('cogs/utils/welc.json') as f:
                welcs = json.loads(f.read())['welcs']
            fmt = random.choice(welcs)
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
    if str(command) == 'eval':
        return
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
        "Hey, Im glad you invited me here, my prefix is **d.**.")
        
def fmt_help(page):
    cmd = ''
    for line in page.splitlines():
        if line.startswith('.'):
            cmd = line.strip('.')
            break
    em = discord.Embed(color=0x00FFFF)
    em.set_author(name='Help - {}'.format(cmd))

async def send_cmd_help(ctx):
    if ctx.invoked_subcommand:
        pages = bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
        for page in pages:
            # page = page.strip('```css').strip('```')


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

@bot.command(name='presence')
async def _set(Type=None,*,thing=None):
    """Change the bot's discord game/stream!"""
    server = len(bot.servers)
    if Type is None:
            await bot.say('Usage: `.presence [game/stream] [message]`')
    else:
        if Type.lower() == 'stream':
            await bot.change_presence(game=discord.Game(name=thing,type=1,url='https://www.twitch.tv/a'),status='online')
            await bot.say('Set presence to. `Streaming {}`'.format(thing))
        elif Type.lower() == 'game':
            await bot.change_presence(game=discord.Game(name=thing))
            await bot.say('Set presence to `Playing {}`'.format(thing))
        elif Type.lower() == 'clear':
            await bot.change_presence(game=None)
            await bot.say('Cleared Presence')
        elif Type.lower() == 'servers':
            await bot.change_presence(game=discord.Game(name='with {} servers'.format(server)))
            await bot.say('**Im now playing with {} servers.**'.format(server))
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

@bot.command(pass_context=True)
@is_owner()
async def _leave_server(ctx, server):
    to_leave = discord.utils.get(bot.servers, id=str(server))
    try:
        await bot.leave_server(to_leave)
    except:
        await self.bot.say('Failed.')
    else:
        await self.bot.say('Successfully left {}'.format(to_leave.name))

@bot.command(pass_context=True)
async def register(ctx):
    server = ctx.message.server
    channel = discord.utils.get(server.channels, name='server-event')
    user = ctx.message.author
    with open('cogs/utils/registrations.txt') as f:
        data = f.read()
        print(data )

    if ctx.message.channel != channel:
        await bot.say('You can only register in {}'.format(channel.mention))
        return
    
    if str(user) in data:
        await bot.delete_message(ctx.message)
        await bot.send_message(user, "You can't register more than once.")
        return
    with open('cogs/utils/registrations.txt','a') as f:
        f.write(str(user)+'\n')
    role = discord.utils.get(server.roles, name='4row')
    await bot.add_roles(user, role)
    await bot.add_reaction(ctx.message, '\u2705')
   
@bot.command(pass_context = True)
async def shutdown(ctx):
    await bot.say('Shutting down, see you later.')
    await bot.logout()
 
if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded: {}'.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Error on load: {}\n{}'.format(extension, exc))
           
@bot.command(pass_context=True, name='eval')
async def _eval(ctx, *, body: str):
    '''Run python scripts on discord!'''
    await to_code_block(ctx, body)
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.message.channel,
        'author': ctx.message.author,
        'server': ctx.message.server,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(content=body)
    stdout = io.StringIO()

    to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

    try:
        exec(to_compile, env)
    except SyntaxError as e:
        return await bot.say(get_syntax_error(e))

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        x = await bot.say('```py\n{}{}\n```'.format(value, traceback.format_exc()))
        try:
            await bot.add_reaction(x, '\U0001f534')
        except:
            pass
    else:
        value = stdout.getvalue()
        
        if TOKEN in value:
            value = value.replace(TOKEN,"[EXPUNGED]")
            
        if ret is None:
            if value:
                try:
                    x = await bot.say('```py\n%s\n```' % value)
                except:
                    x = await bot.say('```py\n\'Result was too long.\'```')
                try:
                    await bot.add_reaction(x, '\U0001f535')
                except:
                    pass
            else:
                try:
                    await bot.add_reaction(ctx.message, '\U0001f535')
                except:
                    pass
        else:
            try:
                x = await bot.say('```py\n%s%s\n```' % (value, ret))
            except:
                x = await bot.say('```py\n\'Result was too long.\'```')
            try:
                await bot.add_reaction(x, '\U0001f535')
            except:
                pass
   




   
bot.run(TOKEN)
