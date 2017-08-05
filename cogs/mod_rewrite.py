import discord
import asyncio
from .ext import commands
from __main__ import send_cmd_help
from .utils import settings

class Moderation:

	def __init__(self, bot):
		self.bot = bot

    def is_mod(ctx):
	    info = settings.config()
	    owner = '319395783847837696'

	    server = ctx.message.server
	    s_owner = server.owner
	    author = ctx.message.author

	    mod = discord.utils.get(server.roles, id=info[server.id]['mod_role'])
	    admin = discord.utils.get(server.roles, id=info[server.id]['admin_role'])

	    if author.id == owner:
	    	return True
	    if author is s_owner:
	        return True
	    if mod in author.roles:
	    	return True
	    if admin in author.roles:
	    	return True

	async def mod_log_entry(self, ctx, type, reason):
		server = ctx.message.server
		

	@commands.command(pass_context=True)
	@commands.check(is_mod)
	async def kick(self, ctx, user : discord.Member, *, reason=None):
		author = ctx.message.author
		if author.top_role > user.top_role:
			try:
				await self.bot.kick(user)
				await self.bot.say('Kicked {} from the server.'.format(user))
			except:
				await self.bot.say("I'm not allowed to do that.")
			else:
				await self.mod_log_entry(ctx, user, 'kick', reason)
		else:
			await self.bot.say('You cant kick people that are higher or equal to you.')









def setup(bot):
	bot.add_cog(Moderation(bot))