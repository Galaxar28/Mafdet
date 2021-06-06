import logging

from discord.ext import commands


class botMaintenance(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    # every command here needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id
    # end of def cog_check

    # cog error handler
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. Join the support discord server if you are having "
                           "any problems. This usage has been logged.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        else:
            logger.warning('cog_command_error: {}'.format(error))
            raise error
    # end of def cog_command_error


    # quitbot - Stop the bot
    # @bot.command(hidden=True)
    @commands.command(hidden=True)
    async def quitbot(self, ctx):
        """"""
        logger.info("Shutting down.")
        await ctx.send("Shutting down...\n\U0001f44b")
        await self.bot.logout()
    # end of def quitbot


def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(botMaintenance(bot))
# end of def setup
