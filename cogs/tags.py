import discord
from discord.ext import commands
import json
import difflib
from .utils import launcher

info = launcher.settings()
mod_role = info['mod_role']

class Tags():
	def __init__(self, bot):
		self.bot = bot

	async def make_tag(self, tag, content, user):
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		if tag in data:
			await self.bot.say('This tag-name already exists.')
		elif tag not in data:
			data[tag] = [content,user.id]
			print(data)
			data = json.dumps(data,indent=2)
			with open('cogs/utils/tags.json', 'w') as f:
				f.write(data)
			await self.bot.say('Successfuly created tag.')

	async def edit_tag(self, tag, content, user):
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)

		if tag not in data:
			possible_matches = difflib.get_close_matches(tag, tuple(data.keys()))
			if not possible_matches:
				await self.bot.say('**Tag not found.**')
			else:
				possible_matches = ['`'+i+'`' for i in possible_matches]
				await self.bot.say(('Tag not found. Did you mean: ' + ', '.join(possible_matches)).strip(', '))

		if data[tag][1] == user or discord.utils.get(user.roles, name=mod_role):
			data[tag] = [content,user.id]
			print(data)
			data = json.dumps(data, indent=2)
			with open('cogs/utils/tags.json', 'w') as f:
				f.write(data)
			await self.bot.say('Successfully edited the tag')
		else:
			await self.bot.say('You are not the owner of this tag.')


	@commands.group(pass_context=True, invoke_without_command=True)
	async def tag(self, ctx, *,name : str):
		if ctx.invoked_subcommand is None:
			data = open('cogs/utils/tags.json').read()
			data = json.loads(data)
			try: 
				d = data[name][0]
				await self.bot.say(d)
			except:
				possible_matches = difflib.get_close_matches(name, tuple(data.keys()))
				if not possible_matches:
					await self.bot.say('**Tag not found.**')
				else:
					possible_matches = ['`'+i+'`' for i in possible_matches]
					await self.bot.say(('Tag not found. Did you mean: ' + ', '.join(possible_matches)).strip(', '))


	@tag.command(pass_context=True, aliases=['create'])
	async def make(self, ctx, tag: str, *, content: str):
		user = ctx.message.author
		await self.make_tag(tag,content,user)

	@tag.command(name='del',pass_context=True, aliases=['d', 'delete'])
	async def _del(self, ctx, name : str):
		user = ctx.message.author
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		if user.id == data[name][1] or discord.utils.get(user.roles, name=mod_role):
			del data[name]
			await self.bot.say('Tag deleted.')
		else:
			await self.bot.say('You cannot delete a tag you do not own.')
		data = json.dumps(data, indent=2)
		with open('cogs/utils/tags.json', 'w') as f:
			f.write(data)

	@tag.command(pass_context=True)
	async def edit(self, ctx, tag: str, *, content):
		user = ctx.message.author
		await self.edit_tag(tag,content,user)

	@commands.command(pass_context=True)
	async def tags(self,ctx):
		data = open('cogs/utils/tags.json').read()
		data = json.loads(data)
		data = ', '.join(data.keys())
		data = data.strip(', ')
		print(data)
		data = '```brainfuck\n'+data+'```'
		print(data)
		await self.bot.say('**List of current tags:**\n'+data)


def setup(bot):
	bot.add_cog(Tags(bot))
