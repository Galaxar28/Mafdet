import logging
from unidecode import unidecode
from discord.ext import commands


class osrrListener(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, msg):
        try:
            logger.info('OSRR : {}'.format(unidecode(msg)))
        except Exception as err:
            logger.info('OSRR error: {}'.format(err))
            logger.info('OSRR error: {}'.format(msg))

def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(osrrListener(bot))
# end of def setup

