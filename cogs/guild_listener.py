import logging
from unidecode import unidecode
from discord.ext import commands


class guildListener(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        # logger.info('OGCU before slice: -{}-'.format(before.name[0:6]))
        # logger.info('OGCU after slice : -{}-'.format(after.name[0:6]))
        if (before.name[0:6] != "online"):
            logger.info('OGCU before: {}'.format(before.name))
            logger.info('OGCU after : {}'.format(after.name))

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        logger.info('OGU before: {}'.format(before))
        logger.info('OGU after : {}'.format(after))

def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(guildListener(bot))
# end of def setup

