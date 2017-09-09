import discord
from discord.ext import commands
import datetime
import time

class Misc():
    
    def __init__(self, bot):
         self.bot = bot
    
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
    
@commands.command(pass_context = True)
async def say(self,ctx, message: str):
    '''Say something as the bot'''
    await self.bot.say(message)
    await self.bot.delete_message(ctx.message)

def setup(bot):
    bot.add_cog(Misc(bot))

