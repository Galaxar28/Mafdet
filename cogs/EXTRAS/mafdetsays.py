import logging
import discord
from datetime import datetime
from discord.ext import commands


class MafdetSays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # every command needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. Join the support discord server if you are having "
                           "any problems. This usage has been logged.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('need to do something here?  Missing Required Argument')
        else:
            logger.warning(error)
    # end of def cog_command_error

    @commands.command(hidden=True)
    @commands.has_permissions(is_owner=True)
    async def mafsays(self, ctx, channel):
        """Make Mafdet say something"""

asdf
asdf
asdf
asdf
asdf
asdf






    
        title = "**Mafdet -- Egyptian goddess of judgement, justice, and execution**"
        color = discord.Colour(0x6da1c2)
        url="http://egyptian-gods.org/egyptian-gods-mafdet/"
        description="Known as \"Slayer of Serpents\" and \"The Great Cat\", Mafdet dates from the First Dynasty of Agent Egypt.  She is the defender against venemous creatures like snakes and scorpions and is the protector of the pharaoh."
        # timestamp=datetime.now()
    
        # embed = discord.Embed(title=title, colour=color, url=url, description=description, timestamp=timestamp)
        embed = discord.Embed(title=title, colour=color, url=url, description=description)
    
        embed.set_image(url="http://maryarrchie.com/wp-content/uploads/2018/12/bastet-goddess.jpg")
    
        # embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.set_author(name="Mafdet", url="https://en.wikipedia.org/wiki/Mafdet", icon_url=self.bot.user.avatar_url)
        # embed.set_author(name="Mafdet", url="https://en.wikipedia.org/wiki/Mafdet", icon_url="https://cdn.discordapp.com/embed/avatars/2.png")
        # embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/1.png")
   
        await ctx.send(embed=embed)
        await ctx.send("Hello, I am Mafdet. My commands start with a `.`\nUse `.help` for help")
    # end of whoismafdet

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(MafdetSays(bot))
# end of def setup

