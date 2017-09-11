import discord
from ext.commands import Bot
from ext import commands
import datetime
import time
import random
import asyncio
import json



class Misc():


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
        msgtime = ctx.message.timestamp.now()
        await (await self.bot.ws.ping())
        now = datetime.datetime.now()
        ping = now - msgtime
        pong = discord.Embed(title='Pong! Response Time:', description=str(ping.microseconds / 1000.0) + ' ms',
                            color=FF3DFE)
        await self.bot.send_message(ctx.message.channel, embed=pong)
        await self.bot.add_reaction(pong, '\U0001f3d3')
             







    
def setup(bot):
    bot.add_cog(Misc(bot))
