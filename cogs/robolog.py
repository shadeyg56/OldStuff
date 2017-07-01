import discord
from discord.ext import commands
import datetime
from .utils import launcher

info = launcher.settings()
admin = info['admin_role']

class Robolog:
	def __init__(self, bot):	
		self.bot = bot

	def getday(self):
		day = None
		day = datetime.datetime.now()
		day = day.strftime("%d/%m/%Y")
		return day

	async def send_cmd_help(self,ctx):
		if ctx.invoked_subcommand:
			pages = self.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
			for page in pages:
				await self.bot.send_message(ctx.message.channel, page)
		else:
			pages = self.bot.formatter.format_help_for(ctx, ctx.command)
			for page in pages:
				await self.bot.send_message(ctx.message.channel, page)

	@commands.group(pass_context=True)
	@commands.has_role(admin)
	async def log(self, ctx):
		"""Robotics Log Commands"""
		if ctx.invoked_subcommand is None:
			await self.send_cmd_help(ctx)

	@log.command(pass_context=True)
	async def entry(self, ctx, *, entry : str):
		"""Create a log entry"""
		date = self.getday()
		msg = open('cogs/utils/robolog.txt').read()
		with open('cogs/utils/robolog.txt','a') as log:
			if date not in msg:
				log.write('\n+ '+date+'\n- '+entry+'\n')
			else:
				log.write('- '+entry+'\n')

		await self.bot.say('Added `{}` to the log'.format(entry))


	@log.command(pass_context=True)
	async def show(self, ctx):
		"""Show the current log"""
		msg = open('cogs/utils/robolog.txt').read()
		log = '```diff\n'+'!---===[ Robotics Log ]===---!\n\n'+(''.join(msg))+'```'
		await self.bot.say(log)

	@log.command(name='del',pass_context=True, aliases=['delete','d'])
	async def del_(self, ctx, index: int = None):
		'''Delete a log entry from the back, or by index (reversed)'''
		log = []
		with open('cogs/utils/robolog.txt') as f:
			for line in f:
				log.append(line)
		if index is None:
			x = log.pop()
			await self.bot.say('Successfully removed `{}` from the log'.format(x[1:].strip()))
			
		else:
			await self.bot.say('Successfully removed `{}` from the log'.format(log[len(log) - index][1:].strip()))
			del log[len(log) - index]
			

		log = ''.join(log)

		with open('cogs/utils/robolog.txt', 'w') as f:
			f.write(log)


def setup(bot):
    bot.add_cog(Robolog(bot))



