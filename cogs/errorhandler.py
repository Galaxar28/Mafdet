import logging

from discord.ext import commands


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            logger.info('CommandErrorHandler on_command_error: {}'.format(error))
            await ctx.send('Unknown command.')


def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(CommandErrorHandler(bot))
# end of def setup

