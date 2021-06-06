import logging
import discord
from datetime import datetime
from discord.ext import commands


class Ping2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ''' everyone can do this
    # every command needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id
    '''

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.reply("Only the owner can use this module. Join the support discord server if you are having "
                           "any problems. This usage has been logged.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply('need to do something here?  Missing Required Argument')
        else:
            logger.warning(error)
    # end of def cog_command_error

    @commands.command()
    async def ping2(self, ctx):
        '''Simple latency test'''
        latency = self.bot.latency
        await ctx.reply("Pong: {}".format(latency))
        logme("info", ctx, "inside ping")
    
    # per-command before_ and after_ invokes, too!
    '''
    @ping.before_invoke
    async def before_ping_command(ctx):
        # do something before the ping command is called
        logger.info('Main: Executing ping.before_invoke')
        pass
    
    @ping.after_invoke
    async def after_ping_command(ctx):
        # do something after the ping command is called
        logger.info('Main: Executing ping.after_invoke')
        pass
    '''

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(Ping2(bot))
# end of def setup

