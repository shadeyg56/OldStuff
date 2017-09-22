import discord
from ext.commands import Bot
from ext import commands
import datetime
import time
import random
import asyncio
import json
from .utils import launcher


class Old_Misc():


    def __init__(self, bot):
        self.bot = bot
        
    poke = pykemon.V1Client()
        
    async def send_cmd_help(self,ctx):
        if ctx.invoked_subcommand:
            pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
            for page in pages:
                await self.bot.send_message(ctx.message.channel, page)     
        else:
           pages = self.bot.formatter.format_help_for(ctx, ctx.command)
           for page in pages:
               await self.bot.send_message(ctx.message.channel, page)
     
    
    @commands.command(pass_context = True)
    async def ping(self,ctx):
        pingtime = time.time()
        ping = time.time() - pingtime
        pong = discord.Embed(title='Pong! Response Time:', description=str(ping), color=0xed)
        await self.bot.say(embed=pong)
        
    @commands.command(pass_context = True)
    async def test(self, ctx):
        await asyncio.sleep(2)
        await self.bot.say('Hello')
        
    @commands.command(pass_context = True)
    async def invite(self, ctx):
        await self.bot.say('**Darkness Invite:** https://discordapp.com/oauth2/authorize?client_id=355189919410421760&scope=bot&permissions=66186303')
                      
    @commands.command(pass_context = True)
    async def suggest(self, ctx, message: str):
        timestamp = ctx.message.timestamp
        server = ctx.message.server
        message = ctx.message.content
        author = ctx.message.author
        channel = self.bot.get_channel('356602525740433408')
        avatar = author.avatar_url
        suggestion = discord.Embed(title='Suggestion', description='{}'.format(message), color=0xed, timestamp=timestamp)
        suggestion.set_author(name=author, icon_url=avatar)
        suggestion.set_footer(text='Sent from {}'.format(server))
        await self.bot.send_message(channel, embed=suggestion)
        await self.bot.say('Suggestion added')
        
    @commands.command(pass_context = True)
    async def support(self, ctx):
        await self.bot.say('**Darkness Support:** https://discord.gg/Jjdp8hf')
                       
    @commands.command(pass_context = True)
    async def info(self, ctx):
        stamp = ctx.message.timestamp
        embed = discord.Embed(title='Darkness Info', color=0xed, timestamp=stamp)
        servers = len(self.bot.servers)                    
        embed.add_field(name='Author', value='<@300396755193954306>')
        embed.add_field(name='Servers', value=servers)
        embed.add_field(name='Prefix', value='d.')
        embed.set_footer(text='Powered by discord.py')
        embed.set_thumbnail(url='http://data.whicdn.com/images/150102219/large.gif')
        embed.add_field(name='Invite', value='https://discordapp.com/oauth2/authorize?client_id=355189919410421760&scope=bot&permissions=66186303')
        embed.add_field(name='Support', value='https://discord.gg/Jjdp8hf')
        embed.add_field(name='GitHub', value='https://github.com/shadeyg56/darkness')
        await self.bot.say(embed=embed)    
        
    @commands.command(pass_context = True)
    async def calc(self,Type=None,*args):
        ans = 0
        try:
            if Type.lower() == 'add':
                for i in args:
                  ans += int(i)
                  await self.bot.say(ans)
        except:
            await self.bot.say('You can only use numbers silly')
            
    @commands.command(pass_context = True)
    async def remind(self, ctx, time: int, task: str, DM=None):
        user = ctx.message.author
        if DM == None:
            time2 = time / 60
            await self.bot.say('Ill remind you to {} in {} minutes'.format(task, time2))
            await asyncio.sleep(time2)
            await self.bot.say('{0.mention} make sure you {}'.format(user, task))
        elif DM == 'true':
             time2 = time / 60
             await self.bot.say('Ill remind you in DM to {} in {} minutes'.format(task, time2))
             await asyncio.sleep(time2)
             await self.bot.send_message(user, 'Make sure you {}'.format(task))
            
    
       
def setup(bot):
    bot.add_cog(Old_Misc(bot))
