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


class Embed():
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True,description='Do .embed to see how to use it.')
    @commands.has_role('Mod')
    async def embed(self, ctx, *, msg: str = None):
        '''Embed complex rich embeds as the bot.'''
        try:
            
            if msg:
                ptext = title = description = image = thumbnail = color = footer = author = None
                timestamp = discord.Embed.Empty
                def_color = False
                embed_values = msg.split('|')
                for i in embed_values:
                    if i.strip().lower().startswith('ptext='):
                        ptext = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('title='):
                        title = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('description='):
                        description = i.strip()[12:].strip()
                    elif i.strip().lower().startswith('desc='):
                        description = i.strip()[5:].strip()
                    elif i.strip().lower().startswith('image='):
                        image = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('thumbnail='):
                        thumbnail = i.strip()[10:].strip()
                    elif i.strip().lower().startswith('colour='):
                        color = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('color='):
                        color = i.strip()[6:].strip()
                    elif i.strip().lower().startswith('footer='):
                        footer = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('author='):
                        author = i.strip()[7:].strip()
                    elif i.strip().lower().startswith('timestamp'):
                        timestamp = ctx.message.timestamp

                    if color:
                        if color.startswith('#'):
                            color = color[1:]
                        if not color.startswith('0x'):
                            color = '0x' + color

                    if ptext is title is description is image is thumbnail is color is footer is author is None and 'field=' not in msg:
                        await self.bot.delete_message(ctx.message)
                        return await self.bot.send_message(ctx.message.channel, content=None,
                                                           embed=discord.Embed(description=msg))

                    if color:
                        em = discord.Embed(timestamp=timestamp, title=title, description=description, color=int(color, 16))
                    else:
                        em = discord.Embed(timestamp=timestamp, title=title, description=description)
                    for i in embed_values:
                        if i.strip().lower().startswith('field='):
                            field_inline = True
                            field = i.strip().lstrip('field=')
                            field_name, field_value = field.split('value=')
                            if 'inline=' in field_value:
                                field_value, field_inline = field_value.split('inline=')
                                if 'false' in field_inline.lower() or 'no' in field_inline.lower():
                                    field_inline = False
                            field_name = field_name.strip().lstrip('name=')
                            em.add_field(name=field_name, value=field_value.strip(), inline=field_inline)
                    if author:
                        if 'icon=' in author:
                            text, icon = author.split('icon=')
                            if 'url=' in icon:
                                print("here")
                                em.set_author(name=text.strip()[5:], icon_url=icon.split('url=')[0].strip(), url=icon.split('url=')[1].strip())
                            else:
                                em.set_author(name=text.strip()[5:], icon_url=icon)
                        else:
                            if 'url=' in author:
                                print("here")
                                em.set_author(name=author.split('url=')[0].strip()[5:], url=author.split('url=')[1].strip())
                            else:
                                em.set_author(name=author)

                    if image:
                        em.set_image(url=image)
                    if thumbnail:
                        em.set_thumbnail(url=thumbnail)
                    if footer:
                        if 'icon=' in footer:
                            text, icon = footer.split('icon=')
                            em.set_footer(text=text.strip()[5:], icon_url=icon)
                        else:
                            em.set_footer(text=footer)
                await self.bot.send_message(ctx.message.channel, content=ptext, embed=em)
            else:
                msg = '''
**Example:** `.embed title=test this | description=some words | color=3AB35E | field=name=test value=test`

You do NOT need to specify every property, only the ones you want.

**All properties and the syntax** (put your custom stuff in place of the <> stuff)

`•` `title=words`
`•` `description=words`
`•` `color=hex_value`
`•` `image=url_to_image` (must be https)
`•` `thumbnail=url_to_image`
`•` `author=words` *or* `author=name=words icon=url_to_image`
`•` `footer=words` *or* `footer=name=words icon=url_to_image`
`•` `field=name=words value=words` (you can add as many fields as you want)
`•` `ptext=words` (pretext e.g. tag)

**NOTE:** After the command is sent, the bot will delete your message and replace it with the embed.
Make sure you have it saved or else you'll have to type it all again if the embed isn't how you want it.

**PS:** Hyperlink text like so: `[text](https://www.whateverlink.com)`

**PPS:** Force a field to go to the next line with the added parameter inline=False
'''
                await self.bot.send_message(ctx.message.channel, msg)
            try:
                await self.bot.delete_message(ctx.message)
            except:
                pass
        except:
            await self.bot.send_message(ctx.message.channel, 'looks like something fucked up.')
               
            

##
##    @commands.command(pass_context=True)
##    @commands.has_role(modrole)
##    async def post_tourney(self,ctx,*,msg : str):
##        user = ctx.message.author
##        server = ctx.message.server
##        announce = discord.utils.get(server.channels,name=tournaments)
##        if msg:
##            name = pword = gems = host = None
##            msg = msg.split('|')
##            for word in msg:
##                if word.strip().lower().startswith('name='):
##                    name = word.strip()[5:].strip()
##                elif word.strip().lower().startswith('pass='):
##                    pword = word.strip()[5:].strip()
##                elif word.strip().lower().startswith('gems='):
##                    gems = word.strip()[5:].strip()
##                elif word.strip().lower().startswith('host='):
##                    host = word.strip()[5:].strip()
##                else:
##                    await self.bot.say('Something went wrong.')
##            emb = await embtourney(user,name,pword,gems,host)
##            await self.bot.send_message(announce,emb)
##            
##    
def setup(bot):
    bot.add_cog(Embed(bot))
