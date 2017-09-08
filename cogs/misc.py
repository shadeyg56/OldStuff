import discord
from ext.commands import Bot
from ext import commands

class Misc:()
  
    def __init__(self, bot):
    
@bot.command(pass_context = True)
async def ping(self, ctx):
    msgtime = ctx.message.timestamp.now()
          await (await self.bot.ws.ping())
          now = datetime.datetime.now()
          ping = now - msgtime
          pong = discord.Embed(title='Pong! Response Time:', description=str(ping.microseconds / 1000.0) + ' ms', color=FF3DFE)
        
          await self.bot.send_message(ctx.message.channel, embed=pong)
          await self.bot.add_reaction(embed=pong, '\U0001f3d3')

