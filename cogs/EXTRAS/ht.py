import logging
import discord
from discord.ext import commands
from random import randint

class happyThanksgiving(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # every command needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('need to do something here?  Missing Required Argument')
        else:
            logger.warning(error)
    # end of def cog_command_error

    @commands.command(hidden=True)
    # @commands.has_permissions(is_owner=True)
    async def ht(self, ctx):
        """Wishes everyone a Happy Thanksgiving"""
        try: 
            pass
            await ctx.message.delete()
        except Exception as error:
            logger.warning('Error deleting posted message: {}'.format(error))
        try:
            # embed = discord.Embed(title="I hope everyone has a happy and safe Thanksgiving!", colour=discord.Colour(0xaf0000), description='sample description goes here')

            embed = discord.Embed(title="I hope everyone has a happy and safe Thanksgiving!", colour=discord.Colour(0xaf0000))

            # embed.set_thumbnail(url="https://www.metmuseum.org/toah/images/hb/hb_30.4.2.jpg") # won't work - filename has
            # underscore _


            f = discord.File("./hb30.4.2.jpg", filename="hb30.4.2.jpg")
            embed.set_image(url="attachment://hb30.4.2.jpg")

            embed.set_author(name=self.bot.mafdetlist[randint(0,len(self.bot.mafdetlist)-1)], icon_url=self.bot.user.avatar_url)

            await ctx.send(file=f, embed=embed)

            logger.info('mafdet said, happy thanksgiving')
        except Exception as error:
            logger.warning('Error sending a message: {}'.format(error))
    # end of setpresence

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(happyThanksgiving(bot))
# end of def setup

