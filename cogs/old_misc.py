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
        pong = discord.Embed(title='Pong! Response Time:', description=str(ping, color=FF3DFE)
        await self.bot.send_message(ctx.message.channel, embed=pong)
        await self.bot.add_reaction(pong, '\U0001f3d3')
        
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
    
             







    
def setup(bot):
    bot.add_cog(Old_Misc(bot))
