import discord
from ext.commands import Bot
from ext import commands

class Mod():


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def mod_test(self,ctx):
        await self.bot.say('The mod cog is working')
 
