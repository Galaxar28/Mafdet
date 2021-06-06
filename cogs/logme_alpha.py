import logging
import discord
from discord.ext import commands


class Customlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def logme(self, ctx, level, myctx, logstr):
        print (f'level is {level}.')
        print (f'ctx is {myctx}.')
        print (f'logstr is {logstr}.')
        logger.info('inside logme!!')
        return TRUE

    @commands.command()
    async def pingme(self, ctx):
        '''Simple command test'''
        await ctx.send("Ping executed!")
        logger.info('inside pingme')
        await self.logme(ctx, 'my info', 'my ctx', 'stuff')
        logger.info('after logme')

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(Customlog(bot))
# end of setup

