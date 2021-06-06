import logging
import discord
from discord.ext import commands


class Presence(commands.Cog, command_attrs=dict(hidden=True)):
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
    @commands.has_permissions(manage_guild=True)
    #async def setpresence(self, ctx, *, pre):
    async def setpresence(self, ctx):
        """Set the bot's presence"""
        try:
            myname = 'for {}help'.format(self.bot.command_prefix)
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=myname))
            logger.info('Setting presence')
        except Exception as error:
            logger.warning('Error setting presence: {}'.format(error))
    # end of setpresence

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(Presence(bot))
# end of def setup

