import discord
import asyncio
from ext import commands
from __main__ import send_cmd_help
from .utils import settings

class Moderation:

    def __init__(self, bot):
        self.bot = bot
        self.path = 'cogs/utils/modlog.json'

    async def mod_log_entry(self, ctx, user, _type, reason):
        '''Making an entry in `modlog.json`'''
        mod_logs = settings.load_json(self.path)
        server = ctx.message.server
        mod = ctx.message.author
        time = ctx.message.timestamp 
        case_num = len(mod_logs.get(server.id)) + 1 # getting case number

        entry = {}
        entry['mod'] = mod.id
        entry['user'] = user.id
        entry['time'] = ctx.message.timestamp.timestamp()
        entry['type'] = _type
        entry['reason'] = reason
        entry['entry_id'] = await self.send_log_entry(ctx, case_num, user, mod, _type, reason)

        mod_logs[server.id][str(case_num)] = entry
        settings.save_json(mod_logs, self.path)
        
    async def send_log_entry(self, ctx, case, user, mod, _type, reason):
        '''Sending the long entry in a mod_log'''
        channel = settings.get_mod_log_channel(ctx)
        if not channel:
            return

        color_conversions = {
            'kick': discord.Color.red(),
            'ban': discord.Color.red(),
            'softban': discord.Color.red(),
            'mute': discord.Color.orange(),
            'warn' : discord.Color.orange(),
            'unban': discord.Color.green()
            }

        title = 'Mod-log Entry | {} | Case {}'.format(_type.title(), case)
        no_reason = 'No current reason. Do `{}reason {}` to set a reason.'.format(ctx.prefix, case)

        reason = reason if reason else no_reason

        log = discord.Embed(color=color_conversions[_type], timestamp=ctx.message.timestamp)
        log.set_author(name=title, icon_url=user.avatar_url or user.default_avatar_url)
        log.add_field(name='User', value=str(user))
        log.add_field(name='Moderator', value=mod.mention)
        log.add_field(name='Reason', value=reason)
        log.set_thumbnail(url=user.avatar_url or user.default_avatar_url)
        log.set_footer(text='User ID: {}'.format(user.id))

        msg = await self.bot.send_message(channel, embed=log)
        return msg.id

    @commands.command(pass_context=True)
    @settings.mod_or_perms(kick_members=True)
    async def kick(self, ctx, user : discord.Member, *, reason=None):
        author = ctx.message.author
        if author.top_role > user.top_role:
            try:
                await self.bot.kick(user)
                await self.bot.say('Kicked {} from the server.'.format(user))
            except:
                await self.bot.say("I'm not allowed to do that.")
            else:
                await self.mod_log_entry(ctx, user, 'kick', reason)
        else:
            await self.bot.say('You cant kick people that are higher or equal to you.')

    @commands.command(pass_context=True)
    @settings.mod_or_perms(ban_members=True)
    async def ban(self, ctx, user : discord.Member, *, reason=None):
        author = ctx.message.author
        if author.top_role > user.top_role:
            try:
                await self.bot.ban(user)
                await self.bot.say('Banned {} from the server.'.format(user))
            except:
                await self.bot.say("I'm not allowed to do that.")
            else:
                await self.mod_log_entry(ctx, user, 'ban', reason)
        else:
            await self.bot.say('You cant ban people that are higher or equal to you.')

    @commands.command(pass_context=True)
    @settings.mod_or_perms(ban_members=True)
    async def softban(self, ctx, user : discord.Member, *, reason=None):
        author = ctx.message.author
        if author.top_role > user.top_role:
            try:
                await self.bot.ban(user)
                await self.bot.unban(author.server, user)
                await self.bot.say('Softbanned {} from the server.'.format(user))
            except:
                await self.bot.say("I'm not allowed to do that.")
            else:
                await self.mod_log_entry(ctx, user, 'softban', reason)
        else:
            await self.bot.say('You cant ban people that are higher or equal to you.')

    @commands.command(pass_context=True)
    @settings.mod_or_perms(ban_members=True)
    async def unban(self, ctx, member : str, *, reason=None):
        '''Unban someone using their user ID or name.'''
        server = ctx.message.server
        try:
            bans = await self.bot.get_bans(server)
        except:
            return await self.bot.say("I'm not allowed to do that.")
        else:
            user = await oself.find_user(ctx, bans, member)
            if not user:
                return
        finally:
            await self.bot.unban(server, user)
            await self.mod_log_entry(ctx, user, 'unban', reason)
            await self.bot.say('Unbanned {} from the server.'.format(user))

    async def find_user(self, ctx, bans, member): 
        channel = ctx.message.channel
        users = [user for user in bans if user.id == member or user.name.lower() == member.lower()]

        if len(users) > 1:
            await self.bot.send_message(channel, 'Multiple users found.')
            return False

        if len(users) < 1:
            await self.bot.send_message(channel, 'User not found.')
            return False

        return users[0]

    @commands.command(pass_context=True)
    @settings.mod_or_perms(manage_messages=True)
    async def warn(self, ctx, user : discord.Member, *, reason=None):
        author = ctx.message.author
        warn_msg = "**You have been warned at {}:**\n" \
                   "{}".format(author.server, reason)

        if author.top_role > user.top_role:
            try:
                await self.bot.send_message(user, warn_msg)
            except:
                pass
            else:
                await self.bot.say('**{}** *has been warned.*'.format(user.name))
                await self.mod_log_entry(ctx, user, 'warn', reason)
        else:
            await self.bot.say('You cant warn people that are higher or equal to you.')

    @commands.command(pass_context=True)
    @settings.mod_or_perms(kick_members=True)
    async def mute(self, ctx, user : discord.Member, *, reason=None):
        author = ctx.message.author
        role = discord.utils.get(author.server.roles, name='Muted')
        if not role:
            return await self.bot.say('You dont have a role called `Muted`')
        if author.top_role > user.top_role:
            if role not in user.roles:
                try:
                    await self.bot.add_roles(user, role)
                    await self.bot.say('Muted {}.'.format(user))
                except:
                    await self.bot.say("I'm not allowed to do that.")
                else:
                    await self.mod_log_entry(ctx, user, 'mute', reason)
            else:
                try:
                    await self.bot.remove_roles(user, role)
                    await self.bot.say('Muted {}.'.format(user.mention))
                except:
                    await self.bot.say("I'm not allowed to do that.")
        else:
            await self.bot.say('You cant mute people that are higher or equal to you.')

    @commands.command(pass_context=True)
    @settings.mod_or_perms(manage_roles=True)
    async def role(self, ctx, user : discord.Member, *, roles):
        if not ctx.message.author.top_role > user.top_role:
            return await self.bot.say("You aren't allowed to do that.")

        roles = [r.lower().strip() for r in roles.split(',')]
        
        
        server = ctx.message.server
        to_assign, to_remove = self.find_roles(ctx, user, roles)
        not_allowed = []

        fmt = ''

        for r in list(set(to_assign + to_remove)):
            if not ctx.message.author.top_role > r:
                try:
                    to_assign.remove(r)
                except:
                    pass
                try:
                    to_remove.remove(r)
                except:
                    pass
                not_allowed.append(r)
                
        if not_allowed:
            fmt += "You aren't allowed to manage these roles: {}\n".format(', '.join(['`'+r.name+'`' for r in not_allowed]))


        if to_assign:
            try:
                fmt += "Added: {}\n".format(', '.join(['`'+r.name+'`' for r in to_assign]))
                await self.bot.add_roles(user, *to_assign)
            except:
                await self.bot.say("I'm not allowed to do that.")

        if to_remove:
            try:
                await self.bot.remove_roles(user, *to_remove)
                fmt += 'Removed: {}\n'.format(', '.join(['`'+r.name+'`' for r in to_remove]))
            except:
                await self.bot.say("I'm not allowed to do that.")

        if to_assign or to_remove:
            await self.bot.say(fmt)


    
    def find_roles(self, ctx, user, roles):
        check = (lambda m: m.name.lower().startswith(role.lower()))
        server = ctx.message.server
        to_assign, to_remove = [], []
        for role in roles:
            if role.startswith('+'):
                role = role.strip('+')
                converted = discord.utils.find(check, server.roles)
                if converted:
                    to_assign.append(converted)
                    continue
            if role.startswith('-'):
                role = role.strip('-')
                converted = discord.utils.find(check, server.roles)
                if converted:
                    to_remove.append(converted)
                    continue
            else:
                converted = discord.utils.find(check, server.roles)
                if converted:
                    if converted in user.roles:
                        to_remove.append(converted)
                    else:
                        to_assign.append(converted)

        to_assign = [role for role in to_assign if role not in user.roles]           
        to_remove = [role for role in to_remove if role in user.roles]

        return (to_assign, to_remove)


    @commands.command(pass_context=True)
    @settings.mod_or_perms(manage_messages=True)
    async def reason(self, ctx, case, * reason):
        mod_logs = settings.load_json(self.path)
        server = ctx.message.server
        if str(case) in mod_logs[server.id]:
            pass


    @commands.command(pass_context=True)
    @settings.mod_or_perms(manage_messages=True)
    async def clean(self, ctx):
        '''Clean up bot messages and command calls.'''

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        async for message in self.bot.logs_from(channel, limit=100):
            if message.author.bot:               
                to_delete.append(message)
            if message.content.startswith(ctx.prefix):
                to_delete.append(message)
        await self.mass_purge(to_delete)
        x = await self.bot.send_message(channel,'Deleted {} messages.'.format(len(to_delete)-1))
        await asyncio.sleep(5)
        await self.bot.delete_message(x)



    @commands.command(pass_context = True,no_pm = True)
    @settings.is_server_owner()
    async def msg(self,ctx,*,msg : str):
        server = ctx.message.server
        '''Message everyone in the server.'''
        if ctx.message.author == ctx.message.server.owner:
            for member in server.members:
                try:
                    await self.bot.send_message(member, '__***Announcement From {}***__\n\n'.format(server.name)+msg)
                    print(member)
                except:
                    print(member, "has DM's turned off")
        else:
            await self.bot.say('Server owner only.')
        

    @commands.command(pass_context=True)
    @settings.mod_or_perms(manage_messages=True)
    async def purge(self, ctx, number: int):
        '''Delete a specified amount of messages.'''

        channel = ctx.message.channel
        author = ctx.message.author
        server = author.server
        is_bot = self.bot.user.bot
        has_permissions = channel.permissions_for(server.me).manage_messages

        to_delete = []

        if not has_permissions:
            await self.bot.say("I'm not allowed to delete messages.")
            return

        async for message in self.bot.logs_from(channel, limit=number+1):
            to_delete.append(message)
        x = await self.bot.send_message(channel,'Deleting messages...')
        await self.mass_purge(to_delete)
        x = await self.bot.edit_message(x,'Deleted {} messages.'.format(len(to_delete)-1))
        await asyncio.sleep(5)
        await self.bot.delete_message(x)

    async def mass_purge(self, messages):
        while messages:
            if len(messages) > 1:
                await self.bot.delete_messages(messages[:100])
                messages = messages[100:]
            else:
                await self.bot.delete_message(messages[0])
                messages = []
            await asyncio.sleep(1.5)







def setup(bot):
    bot.add_cog(Moderation(bot))
