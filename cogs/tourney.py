import discord
from discord.ext.commands import Bot
from discord.ext import commands
import datetime
import time
import configparser
from .utils import config



info = config.settings('COGS')

tournaments = info['tournaments']
staffchat = info['admin_channel']
modrole = info['mod_role']


class Tournament():
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

    async def embtourney(self,user,name,pword,gems,host):

        images = {'100':['https://i.imgur.com/5MY1h9r.png',0xdf830e],
                  '500':['https://i.imgur.com/YtQp90c.png',0xdfdf0e],
                  '2000':['https://i.imgur.com/f1LOr4q.png',0x16db36],
                  '10000':['https://i.imgur.com/vKQV78t.png',0x8416db]}
        image = images[gems][0]
        color = images[gems][1]
        
        desc = '```mkd\n> THE TOURNAMENT WILL START SOON.\n> WIN THE THE TOURNAMENT TO GET A ROLE.```'
        name = '```prolog\n'+name+'```'
        pword = '```fix\n'+pword+'```'
        gems = '```py\n'+gems+'```'
        host = '```css\n'+host+'```'
        
        emb = discord.Embed(color=color,description=desc)
        emb.add_field(name='Name',value=name)
        emb.add_field(name='Password',value=pword)
        emb.add_field(name='Gems',value=gems)
        emb.add_field(name='Host',value=host)
        emb.set_author(name='SERVER TOURNAMENT',icon_url=user.avatar_url)
        emb.set_image(url=image)
        
        return emb

    async def modtourney(self,user,name,pword,gems,host):
            
        desc = '**{}** submiited a tournament. `disapprove` / `approve`'.format(user.name)
        name = '`'+name+'`'
        pword = '`'+pword+'`'
        gems = '`'+gems+'`'
        host = '`'+host+'`'
        color = 0x00ff00
        
        emb = discord.Embed(color=color,description=desc)
        emb.add_field(name='Name',value=name)
        emb.add_field(name='Password',value=pword)
        emb.add_field(name='Gems',value=gems)
        emb.add_field(name='Host',value=host)
        emb.set_author(name='Tournament Submission',icon_url=user.avatar_url)
        emb.set_thumbnail(url='http://vignette4.wikia.nocookie.net/clashroyale/images/a/a7/TournamentIcon.png')
        emb.set_footer(text='User ID: '+str(user.id))
        return emb
    
    @commands.group(pass_context=True,description='Tournament submission commands!')
    async def tournament(self,ctx):
        '''Exclusive Clash Royale tournament commands.'''
        if ctx.invoked_subcommand is None:
            await self.send_cmd_help(ctx)


    @tournament.command(pass_context=True,description = 'Request to post a tourney. ')
    async def submit(self,ctx):
        '''Submit a tournament interactively'''
        server = ctx.message.server
        user = ctx.message.author
        channel = ctx.message.channel
        staff = discord.utils.get(server.roles,name=modrole)
        staff = staff.mention
        admin = discord.utils.get(server.channels,name=staffchat)
        announce = discord.utils.get(server.channels,name=tournaments)
        await self.bot.say('**Welcome to the tournament submission system.** \n \n*Type the name of the tournament:* ')
        name = await self.bot.wait_for_message(timeout=15,author=user,channel=channel)
        if name:
            await self.bot.say('*Type the password of the tournament:*')
            pword = await self.bot.wait_for_message(timeout=15,author=user,channel=channel)
            if pword:
                await self.bot.say('*How many gems is this tournament?*')
                gemtype = ['100','500','2000','10000']
                gems = await self.bot.wait_for_message(timeout=15,author=user,channel=channel)
                if gems:
                    gems = gems.content
                    if gems not in gemtype:
                        while gems not in gemtype:
                            await self.bot.say('*Enter a valid number of gems.*')
                            gems = await self.bot.wait_for_message(timeout=15,author=user,channel=channel)
                            gems = gems.content
                            if gems == None:
                                break                   
                    else:
                        pass
                    
                    await self.bot.say('*Who is the host of the tournament?*')
                    host = await self.bot.wait_for_message(timeout=15,author=user,channel=channel)
                    if host:
                        if host.content.lower() == 'me':
                            host = user.name
                        else:
                            host = host.content
                        
                        await self.bot.say('Thank you, your tournament has been submitted.')
                        name = name.content
                        pword = pword.content
                        modEmbed = await self.modtourney(user,name,pword,gems,host)
                        annEmbed = await self.embtourney(user,name,pword,gems,host)
                        await self.bot.send_message(admin,staff,embed=modEmbed)
                        status = False
                        lis = ['approve','disapprove']
                        
                        def is_me(msg):
                            return msg.author != self.bot.user
                        approval = await self.bot.wait_for_message(channel=admin,check=is_me)
                        while approval:
                            if approval.content.lower() == 'approve':
                                await self.bot.send_message(admin,'*Who would you like to tag?* `everyone`,`here` or `none`')
                                tag = await self.bot.wait_for_message(timeout=15,channel=admin,check=is_me)
                                if tag.content == 'everyone':
                                    tag = '@everyone'
                                elif tag.content == 'here':
                                    tag = '@here'
                                else:
                                    tag = None
                                await self.bot.send_message(admin,'*Sending the tournament...*')
                                await self.bot.send_message(announce,tag,embed=annEmbed)
                                break
                            elif approval.content.lower() == 'disapprove':
                                await self.bot.send_message(admin,'*Tournament disapproved.*')
                                break
                            else:
                                await self.bot.send_message(admin, '*Enter a valid answer.*')
                                approval = await self.bot.wait_for_message(channel=admin,check=is_me)                           
                    else:
                        await self.bot.say('Submission cancelled.')
                else:
                    await self.bot.say('Submission cancelled.')
            else:
                await self.bot.say('Submission cancelled.')
        else:
            await self.bot.say('Submission cancelled.')


    @tournament.command(pass_context=True,description='.tournament post name=name | pass=pass | gems=gems | host=host | tag=tag')
    @commands.has_role(modrole)
    async def post(self,ctx,*,msg : str):
        '''Lets moderators post tournaments.'''
        user = ctx.message.author
        server = ctx.message.server
        announce = discord.utils.get(server.channels,name=tournaments)
        if msg:
            name = pword = gems = host = tag = None
            msg = msg.split('|')
            for word in msg:
                if word.strip().lower().startswith('name='):
                    name = word.strip()[5:].strip()
                elif word.strip().lower().startswith('pass='):
                    pword = word.strip()[5:].strip()
                elif word.strip().lower().startswith('gems='):
                    gems = word.strip()[5:].strip()
                elif word.strip().lower().startswith('host='):
                    host = word.strip()[5:].strip()
                elif word.strip().lower().startswith('tag='):
                    tag = word.strip()[4:].strip()
                else:
                    await self.bot.say('Something went wrong.')
            if tag == 'everyone':
                tag = '@everyone'
            elif tag == 'here':
                tag = '@here'
            else:
                tag = None
            emb = await self.embtourney(user,name,pword,gems,host)
            await self.bot.send_message(announce,tag,embed=emb)
            
        else:
            await self.bot.say('Usage: `.post_tourney name=name | pass=pass | gems=gems | host=host | tag=tag`')

            

    
def setup(bot):
    bot.add_cog(Tournament(bot))
