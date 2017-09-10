import discord
from discord.ext import commands
from .utils import asyncio

class KatCog:
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context = True)
  async def hi(self, ctx, user: discord.Member):
    await self.bot.say('Hello!!')
    text = 'test'
    await self.bot.send_message(user, text)

  @commands.command(pass_context = True)
  async def copycat(self, ctx, *, message: str):
    '''Copy what you just said'''
    await self.bot.say(message)
    await self.bot.add_reaction(ctx.message, '')

  @commands.command(pass_context = True)
  async def meme(self, ctx, *, message : str=None):
    '''Post certain memes'''
    doge=discord.Embed(color=0xed, description='Doge')
    list=discord.Embed(title='Memes:', description='Doge\nFeelsBadMan', color=0xed)
    doge.set_image(url="http://i0.kym-cdn.com/entries/icons/mobile/000/013/564/doge.jpg")
    pepe=discord.Embed(color=0xed, description='FeelsBadMan')
    if 'doge' in message:
      await self.bot.say(embed=doge)
    if 'list' in message:
      await self.bot.say(embed=list)
    if 'FeelsBadMan' in message:
      await self.bot.say(embed=pepe)
      
  @commands.command(pass_context = True)
  async def sleeping(self,ctx):
      '''Automatically set your presence to sleeping'''
      name = ctx.message.author
      await bot.change_presence(game.Discord(name='Sleeping',type=1,url='https://www.twitch.tv/sleeping'),status='online')
      await self.bot.say('{} is now sleeping.'.format(name.name))
      
  @commands.command(no_pm = True, pass_context = True)
  async def mute(self, ctx, member: discord.Member):
      '''Mute a member'''
      server_roles = [role for role in ctx.message.server.roles if not role.is_everyone]
      muted = discord.utils.get(server_roles, name='Muted')
      if not discord.utils.get(member.roles, name='Mod'):
            if not discord.utils.get(member.roles, name='Muted'):
                try:
                    await self.bot.add_roles(member,muted)
                    await self.bot.say('{0.mention} has been muted.'.format(member))
                except discord.Forbidden:
                    await self.bot.say('You dont have the perms for that. Get rekt.')            
                    
                        
  @commands.command(no_pm = True, pass_context = True)
  async def unmute(self, ctx, member: discord.Member):
      '''Unmute a member'''
      server_roles = [role for role in ctx.message.server.roles if not role.is_everyone]
      unmuted = discord.utils.get(server_roles, name='Muted')
      if not discord.utils.get(member.roles, name='Mod'):
            if not discord.utils.get(member.roles, name='Muted'):
                try:
                    await self.bot.remove_roles(member,unmuted)
                    await self.bot.say('{0.mention} has been muted.'.format(member))
                except discord.Forbidden:
                    await self.bot.say('Stop trying to unmute your friend when you dont even have perms')            
                                       
  @commands.command(pass_context = True)
  async def troll(self, ctx, member: discord.Member):
      '''Tag someone then auto delete it'''
      await self.bot.edit_message(ctx.message, '{0.mention}'.format(member))
      await self.bot.delete_message(ctx.message)
      if '@everyone' in ctx.message:
                                   await self.bot.delete_message(ctx.message)     

  @commands.command(pass_context = True)
  async def warn(self, ctx, user: discord.Member=None, reason=None):
      warning = 'You have been warned in **{}** by **{}** for: **{}**'
      server = ctx.message.server
      author = ctx.message.author
      await self.bot.say('**{}** has been warned'.format(user))
      await self.bot.send_message(user, warning.format(server, author, reason))
      await self.bot.delete_message(ctx.message)
    
                                
def setup(bot):
    bot.add_cog(KatCog(bot))
