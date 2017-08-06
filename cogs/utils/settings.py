import json
import discord
from ext import commands


def bot():
    config = open("cogs/utils/t_config.json").read()
    config = json.loads(config)
    return config['bot']

def config():
    config = open("cogs/utils/t_config.json").read()
    config = json.loads(config)
    return config

def settings():
    config = open("cogs/utils/config.json").read()
    config = json.loads(config)
    return config

def get_mod_log_channel(ctx):
    server = ctx.message.server
    with open('cogs/utils/t_config.json') as f:
        id = json.load(f)[ctx.message.server.id].get('mod_log')
    if id:
        return discord.utils.get(server.channels, id=id)

def get_mod_logs():
    with open('cogs/utils/modlog.json') as f:
        return json.load(f)

def load_json(PATH):
    with open(PATH) as f:
        return json.load(f)

def save_json(data, PATH):
    with open(PATH, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))


def is_server_owner():

    def pred(ctx):
        return ctx.message.author is ctx.message.server.owner or ctx.message.author.id == '319395783847837696'

    return commands.check(pred)

def check_permissions(ctx, perms):

    if not perms:
        return False

    channel = ctx.message.channel
    author = ctx.message.author
    resolved = channel.permissions_for(author)
    return all(getattr(resolved, name, None) == value for name, value in perms.items())

def mod_or_perms(**perms):
    
    def predicate(ctx):
        if check_permissions(ctx, perms):
            return True

        info = config()
        owner = '319395783847837696'
        server = ctx.message.server
        s_owner = server.owner
        author = ctx.message.author

        mod = discord.utils.get(server.roles, id=info[server.id]['mod_role'])
        admin = discord.utils.get(server.roles, id=info[server.id]['admin_role'])

        if author.id == owner:
            return True
        if author is s_owner:
            return True
        if mod in author.roles:
            return True
        if admin in author.roles:
            return True

    return commands.check(predicate)


