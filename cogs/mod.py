import discord
from ext.commands import Bot
from ext import commands
from .utils import launcher

class Mod():


    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context = True)
    async def mod_test(self,ctx):
        await self.bot.say('The mod cog is working')
        
    def mod(ctx):
        info = launcher.config()
        server = ctx.message.server
        s_owner = server.owner
        modrole = discord.utils.get(server.roles, id=info[server.id]['mod_role'])
        adminrole = discord.utils.get(server.roles, id=info[server.id]['admin_role'])
        author = ctx.message.author
        def is_owner(ctx):
            return ctx.message.author.id == owner
        if author is s_owner:
            return True
        if is_owner(ctx):
            return True
        if modrole:
            modrole = modrole.name
        if adminrole:
            adminrole = adminrole.name
        if discord.utils.get(author.roles,name=adminrole):
            return True
        return discord.utils.get(author.roles,name=modrole) 
    
    @commands.command(pass_context = True)
    async def kick(self, ctx, member: discord.Member):
        if not ctx.message.author.server_permissions.kick_members:
            self.bot.kick(member)
            await self.bot.say('{} was kicked'.format(member))
                      
                           
                           
    
        
        
def setup(bot):
    bot.add_cog(Mod(bot))
 
