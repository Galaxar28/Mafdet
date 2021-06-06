import logging
import discord
from discord.ext import commands


class delMsg(commands.Cog):
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

    @commands.command()
    # @commands.has_permissions(manage_guild=True)
    async def delmessage(self, ctx, *, msg):
        """Create a self-deleting message"""
        try: 
            await ctx.message.delete(delay=5)
        except Exception as error:
            logger.warning('Error deleting posted message: {}'.format(error))
        try:
            await ctx.send(msg, delete_after=10)
            logger.info('sent self deleting message')
        except Exception as error:
            logger.warning('Error sending a message: {}'.format(error))
    # end of setpresence

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(delMsg(bot))
# end of def setup

