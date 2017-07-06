import discord
from discord.ext.commands import Bot
from discord.ext import commands
import datetime
import time
import random
from PythonGists import PythonGists
import json
from .utils import launcher

info = launcher.bot()
owner = info['owner']


class Info():


    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context = True, description = 'See the date and time a user joined the server',no_pm=True)
    async def joined(self,ctx, member : discord.Member = None):
        """Says when a member joined."""
        if member is None:
            member = ctx.message.author
        server = member.server
        date = str(member.joined_at)[:10]
        time = str(member.joined_at)[11:16]
        msg = '{0.mention} joined at {1}'.format(member,date)
        emb = discord.Embed(color=0x00ffff)
        emb.add_field(name='Date',value=date,inline=True)
        emb.add_field(name='Time',value=time,inline=True)
        await self.bot.send_message(server, embed=emb)
        
    @commands.command(pass_context=True,aliases=['s','serverinfo','si'])
    async def server(self, ctx):
        '''See information about the server.'''
        server = ctx.message.server
        online = len([m.status for m in server.members
                      if m.status == discord.Status.online or
                      m.status == discord.Status.idle])
        total_users = len(server.members)
        text_channels = len([x for x in server.channels
                             if x.type == discord.ChannelType.text])
        voice_channels = len(server.channels) - text_channels
        passed = (ctx.message.timestamp - server.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(server.created_at.strftime("%d %b %Y %H:%M"),
                                passed))
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)

        data = discord.Embed(
            description=created_at,
            colour=discord.Colour(value=colour))
        data.add_field(name="Region", value=str(server.region))
        data.add_field(name="Users", value="{}/{}".format(online, total_users))
        data.add_field(name="Text Channels", value=text_channels)
        data.add_field(name="Voice Channels", value=voice_channels)
        data.add_field(name="Roles", value=len(server.roles))
        data.add_field(name="Owner", value=str(server.owner))
        data.set_footer(text="Server ID: " + server.id)

        if server.icon_url:
            data.set_author(name=server.name, icon_url=server.icon_url)
            data.set_thumbnail(url=server.icon_url)
        else:
            data.set_author(name=server.name)

        try:
            await self.bot.say(embed=data)
        except discord.HTTPException:
            await self.bot.say("I need the `Embed links` permission "
                               "to send this")

        
    @commands.command(pass_context=True,aliases=['ui','info','user'],description='See user-info of someone.')
    async def userinfo(self,ctx, user: discord.Member = None):
        '''See information about a user or yourself.'''
        server = ctx.message.server
        if user:
            pass
        else:
            user = ctx.message.author
        avi = user.avatar_url
        if avi:
            pass
        else:
            avi = user.default_avatar_url
        roles = sorted([x.name for x in user.roles if x.name != "@everyone"])
        if roles:
            roles = ', '.join(roles)
        else:
            roles = 'None'
        time = ctx.message.timestamp
        desc = '{0} is {1} right now.'.format(user.name,user.status)
        member_number = sorted(server.members,key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(colour=0x00fffff,description = desc,timestamp=time)
        em.add_field(name='Nick', value=user.nick, inline=True)
        em.add_field(name='Member No.',value=str(member_number),inline = True)
        em.add_field(name='Account Created', value=user.created_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Join Date', value=user.joined_at.__format__('%A, %d. %B %Y'))
        em.add_field(name='Roles', value=roles, inline=True)
        em.set_footer(text='User ID: '+str(user.id))
        em.set_thumbnail(url=avi)
        em.set_author(name=user, icon_url='http://site-449644.mozfiles.com/files/449644/logo-1.png')
        await self.bot.send_message(ctx.message.channel, embed=em)

    @commands.command(pass_context=True,aliases=['av','dp'])
    async def avatar(self,ctx, user: discord.Member = None):
        '''Returns ones avatar URL'''
        if user:
            pass
        else:
            user = ctx.message.author
        avi = user.avatar_url
        if avi:
            pass
        else:
            avi = user.default_avatar_url
        colour = ("#%06x" % random.randint(0, 0xFFFFFF))
        colour = int(colour[1:], 16)

        em = discord.Embed(color=colour)
        em.set_image(url=avi)
        await self.bot.say(embed=em)

    async def send_cmd_help(self,ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)
        else:
            pages = self.bot.formatter.format_help_for(ctx, ctx.command)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)

    def owner_only():
        return commands.check(lambda ctx: ctx.message.author == ctx.message.server.owner)

    def is_owner():
        return commands.check(lambda ctx: ctx.message.author.id == owner)

    @commands.group(pass_context=True)
    @is_owner()
    async def backup(self,ctx):
        """Backup raw data for storage"""
        if ctx.invoked_subcommand is None:
            await self.send_cmd_help(ctx)

    @backup.command(pass_context=True)
    async def tags(self,ctx):
        tags = open('cogs/utils/tags.json').read()
        url = PythonGists.Gist(description='All current tags', content=str(tags), name='tags.txt')
        em = discord.Embed(description="[raw tags data]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)

    @backup.command(pass_context=True)
    async def config(self,ctx):
        cfg = open('cogs/utils/t_config.json').read()
        url = PythonGists.Gist(description='All current tags', content=str(cfg), name='config.txt')
        em = discord.Embed(description="[raw config data]({})".format(url),color=0x00ffff)
        await self.bot.say(embed=em)






def setup(bot):
    bot.add_cog(Info(bot))
