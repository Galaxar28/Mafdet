import logging
import discord
from discord.ext import commands

class logme2(commands.Cog):
    def __init__(self):
        logme_is_active = 1

    def logme2(self, level, myctx, logstr):
        print (f'level is {level}.')
        print (f'ctx is {myctx}.')
        print (f'logstr is {logstr}.')
        logger.info('inside logme2!!')

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(logme2(bot))

# end of setup

