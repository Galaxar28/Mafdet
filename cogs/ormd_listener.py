import logging
from unidecode import unidecode
from discord.ext import commands


class ormdListener(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        try:
            mymessageid = payload.message_id
            myguild = self.bot.get_guild(payload.guild_id)
            mychannel = myguild.get_channel(payload.channel_id)
            try:
                mymessage = await mychannel.fetch_message(payload.message_id)
            except Exception as err:
                mymessage = payload.cached_message
                logger.info('ORMD : using cached_message')

            deletedInfo  = "{} deleted a message from {} #{}".format(mymessage.author.name,myguild.name,mychannel.name)
            deletedInfo += "\n--- Message Start ---\n{}\n--- Message End ---".format(mymessage.content)
            logger.info('ORMD : {}'.format(deletedInfo))
        except Exception as error:
            logger.info('ORMD error: {}'.format(error))

def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(ormdListener(bot))
# end of def setup

