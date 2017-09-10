from ext import commands
import discord

def to_keycap(c):
    return '\N{KEYCAP TEN}' if c == 10 else str(c) + '\u20e3'

class Polls:
    """Poll voting system."""

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
async def test(self,ctx):
    await bot.say('hi')
                
            
def setup(bot):
    bot.add_cog(Polls(bot))
