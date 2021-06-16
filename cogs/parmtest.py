# additional typing checking from
# https://github.com/FelixTheC/strongtyping
# from strongtyping.strong_typing import match_typing

import logging
import discord
from discord.ext import commands

class parmTest(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('error: Missing Required Argument')
        elif isinstance(error, commands.ConversionError):
            await ctx.send('conversion error-converter: {}'.format(error.converter))
            await ctx.send('conversion error-original: {}'.format(error.original))
        elif isinstance(error, commands.BadArgument):
            await ctx.send('conversion error-bad argument: {}'.format(error))
        else: 
            logger.warning("unknown error: {}".format(error))

    @commands.command()
    @commands.is_owner()
    # @match_typing # see import at top of file for info
    async def pt(self, ctx, member: discord.Member):
        await ctx.send('member: {}'.format(member.display_name))
    
    @pt.error
    async def pt_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send('Only the bot owner can use the {} command'.format(ctx.command.name))
        elif isinstance(error, commands.ConversionError):
            await ctx.send('pt.error-conversionerror: {}'.format(error))
        elif isinstance(error, commands.BadArgument):
            # we were expecting a discord.Member.  If we have a 
            # BadArgument, then we didn't find the member.
            await ctx.send('Member {} not found.'.format(member))
        else:
            await ctx.send('pt.error: {}'.format(error))
            # read up on how to use pdb before using this!
            # it STOPS execution and debugs in the console
            # import pdb
            # pdb.post_mortem()

            template = "An exception of type \'{0}\' occurred.\nArguments: {1!r}"
            message = template.format(type(error).__name__, error.args)
            logger.info(message)
            await ctx.send(message)
 
            # import traceback
            # import sys
            # traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

        # don't return from this error handler - it would prevent higher-level error
        # handlers (like cog_command_error) from processing the exception
        pass

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(parmTest(bot))
# end of setup

