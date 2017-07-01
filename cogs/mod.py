import discord
import datetime
import time
from discord.ext import commands
import asyncio
from .utils import launcher

info = launcher.settings()
mod_role = info['mod_role']

class Mod():
    def __init__(self, bot):
        self.bot = bot

    async def modlog(self,Type,user,moderator,time,reason=None):
        channel = discord.Object(id=325718146243624970)
        clr = 0
        red = ['Kick','Ban','Soft-Ban']
        orange = ['Warn','Mute']
        green = ['Unban']
        if Type in red:
            clr = 0xbb3f27
        elif Type in orange:
            clr = 0xaa8f22
        elif Type in green:
            clr = 0x24b32a
        avi = ''
        if Type == 'Unban':
            avi = None
            mem = await self.bot.get_user_info(user)
            embed = discord.Embed(colour=clr,timestamp=time)
            embed.add_field(name='User',value=mem)
            embed.add_field(name='Mod',value=moderator.mention)
            embed.add_field(name='Type',value=Type)
            embed.add_field(name='Reason',value=reason)
            embed.set_author(name='Mod-Log Entry: ')
            embed.set_footer(text='ID: '+user)
            await self.bot.send_message(channel,embed=embed)
        else:
            if user.avatar_url:
                avi = user.avatar_url
            else:
                avi = user.default_avatar_url

        embed = discord.Embed(colour=clr,timestamp=time)
        embed.add_field(name='User',value=user.mention)
        embed.add_field(name='Mod',value=moderator.mention)
        embed.add_field(name='Type',value=Type)
        embed.add_field(name='Reason',value=reason)
        embed.set_author(name='Mod-Log Entry: '+user.name,icon_url=avi)
        embed.set_footer(text=('ID: '+user.id))
        await self.bot.send_message(channel,embed=embed)


    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def kick(self,ctx, member : discord.Member,*,reason=None):
        '''Kick someone out of the server.'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            if not discord.utils.get(member.roles, name='Mod'):
                await self.bot.kick(member)
                await self.bot.say('Done. That felt good.')
                await self.modlog('Kick',member,mod,time,reason)
            else:
                await self.bot.say('I cant kick a Mod.')

        except discord.Forbidden:
            await self.bot.say("Bot ain't got the perms lad.")


    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def ban(self,ctx, member : discord.Member,*,reason=None):
        '''Ban someone from the server'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            if not discord.utils.get(member.roles, name='Mod'):
                await self.bot.ban(member)
                await self.bot.say('Done. Enough Chaos.')
                await self.modlog('Ban',member,mod,time,reason)
            else:
                await self.bot.say('Dont try.')

        except discord.Forbidden:
            await self.bot.say("Bot ain't got the perms lad.")

    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def softban(self,ctx, member : discord.Member,*,reason=None):
        '''Kick someone out and delete their messages.'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            if not discord.utils.get(member.roles, name='Mod'):
                await self.bot.ban(member)
                await self.bot.unban(member.server,member)
                await self.bot.say('Done. Eleeectronss.')
                await self.modlog('Soft-Ban',member,mod,time,reason)
            else:
                await self.bot.say('Dont try.')

        except discord.Forbidden:
            await self.bot.say("Bot ain't got the perms lad.")

    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def unban(self,ctx,member : str,*,reason=None):
        '''Unban someone using their user ID.'''
        server = ctx.message.server
        mem = discord.Object(id=member)
        mod = ctx.message.author
        time = ctx.message.timestamp
        try:
            await self.bot.unban(server, mem)
            await self.bot.say('Done. Eleeectronss.')
            await self.modlog('Unban',member,mod,time,reason)
        except discord.Forbidden:
            await self.bot.say("Bot ain't got the perms lad.")

    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def mute(self,ctx,member: discord.Member,*,reason=None):
        '''Mute or Unmute someone.'''
        server = ctx.message.server
        role = discord.utils.get(server.roles, name='Muted')
        mod = ctx.message.author
        time = ctx.message.timestamp
        if not discord.utils.get(member.roles, name='Mod'):
            if not discord.utils.get(member.roles, name='Muted'):
                try:
                    await self.bot.add_roles(member,role)
                    await self.bot.say('{0.mention} is now muted.'.format(member))
                    await self.modlog('Mute',member,mod,time,reason)
                except discord.Forbidden:
                    await self.bot.say('I dont have the perms.')
            else:
                await self.bot.remove_roles(member,role)
                await self.bot.say('{0.mention} can now speak.'.format(member))
        else:
            await self.bot.say('You cant mute mods.')

    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
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
        x = await self.bot.send_message(channel,'Deleting messages.')
        x = await self.bot.edit_message(x,'Deleting messages..')
        x = await self.bot.edit_message(x,'Deleting messages...')
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


    @commands.command(pass_context = True,no_pm = True)
    @commands.has_role(mod_role)
    async def msg(self,ctx,*message):
        '''Message everyone in the server.'''
        if ctx.message.author == ctx.message.server.owner:
                for server in self.bot.servers:
                    for member in server.members:
                        msg = ' '.join(message)
                        try:
                            await self.bot.send_message(member, msg)
                            print(member)
                        except:
                            print(member, "has DM's turned off")
        else:
            await self.bot.say('Only the server owner can do this.')

    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def warn(self,ctx, member : discord.Member=None,*,reason=None):
        '''Warn someone in the server.'''
        mod = ctx.message.author
        time = ctx.message.timestamp
        channel = discord.Object(id=325718146243624970)
        avi = ''
        if member.avatar_url:
            avi = member.avatar_url
        else:
            avi = member.default_avatar_url
        if not discord.utils.get(member.roles, name='Mod'):
            await self.bot.send_message(member,'**You have been warned by {}:** *{}*'.format(mod.name,reason))
            await self.bot.say('{} has been warned.'.format(member.mention))            
            embed = discord.Embed(colour=0xaa8f22,timestamp=time)
            embed.add_field(name='User',value=member.mention)
            embed.add_field(name='Mod',value=mod.mention)
            embed.add_field(name='Warn',value=reason)
            embed.set_author(name='User Warn: '+member.name,icon_url=avi)
            embed.set_footer(text=('ID: '+member.id))
            await self.bot.send_message(channel,embed=embed)
        else:
            await self.bot.say('You cant warn mods dummy.')


    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
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
            if message.author.id == self.bot.user.id:               
                to_delete.append(message)
            if message.content.startswith('.'):
                to_delete.append(message)
        await self.mass_purge(to_delete)
        x = await self.bot.send_message(channel,'Deleted {} messages.'.format(len(to_delete)-1))
        await asyncio.sleep(5)
        await self.bot.delete_message(x)
           
    @commands.command(pass_context=True)
    @commands.has_role(mod_role)
    async def role(self,ctx, member: discord.Member,*,roles=None):
        '''Give a role or a list of roles to someone.'''
        roles = roles.split(',')
        roles = [role.lower().strip() for role in roles]        
        top = ctx.message.author.top_role
        server = ctx.message.server
        channel = ctx.message.channel
        sroles = {}
        to_assign = []
        for i in server.roles:
            x = i.name.lower()
            sroles[x] = i
        for role in roles:
            for key in sroles:
                if key.startswith(role):
                    assign = sroles[key]
                    to_assign.append(assign)
                    break
                else:
                    pass
        if to_assign:
            x = await self.bot.send_message(channel,'`Assigning Roles...`')
            msg = ''
            for role in to_assign:
                if top > role:
                    if role not in member.roles:
                        await self.bot.add_roles(member, role)
                        msg += ', `Added {}`'.format(role)
                        msg = msg.strip(', ')
                        x = await self.bot.edit_message(x,msg)
                    else:
                        await self.bot.remove_roles(member, role)
                        msg += ', `Removed {}`'.format(role)
                        msg = msg.strip(', ')
                        x = await self.bot.edit_message(x,msg)
                else:
                    await self.bot.say('You cant assign roles higher than yourself.')
        else:
            await self.bot.say('Cant find any roles.')
                        
                    
        
        


def setup(bot):
    bot.add_cog(Mod(bot))
