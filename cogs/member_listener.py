import logging
from unidecode import unidecode
from discord.ext import commands

class memberListener(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        # logger.info('New member: [{}] {}'.format(member.guild.name, member.name))
        # move this to on_member_update when the new user verifies
        mychannel = member.guild.system_channel
        if (member.bot):
            logger.info('Guild: {} | Bot added to the server: {}'.format(member.guild.name, member.name))
            msg = 'A bot has been added to the server: {}'.format(member.display_name)
            await mychannel.send(msg)
        else:
            logger.info('Guild: {} | New member joined (pending): {}'.format(member.guild.name, member))
            # don't send the message now, the new member won't see it till s/he accepts the rules.
            # msg = 'Welcome {}!'.format(member.mention)
            # msg = 'Welcome {}!'.format(member.display_name)
            # msg += "\nPlease tell us your STFC in-game name, alliance, and rank."

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # logger.info('Member update: [{}] {}'.format(before.guild.name, before.name))

        # check for new members: if their pending flag changes, then they have verified
        if (before.pending == True):
            if (after.pending == False):
                logger.info('Guild: {} | Member now verified: {}'.format(after.guild.name, after))

                # Send the welcome message and ask for alliance info
                mychannel = after.guild.system_channel
                msg = 'Welcome {}!'.format(after.display_name)
                msg += "\nPlease tell us your STFC in-game name, alliance, and rank."
                await mychannel.send(msg)
            else:
                logger.info('Guild: {} | Member updated but still pending: {}'.format(after.guild.name, after))
        elif (before.status != after.status):
            # if it's just a status update, do nothing
            # logger.info("status update")
            # logger.info('[{}] {} Before: {} After: {}'.format(before.guild.name, before.name, before.status, after.status))
            garbage = 0
        elif (before.raw_status != after.raw_status):
            # if it's just a status update, do nothing
            # logger.info("raw_status update")
            # logger.info('[{}] {} Before: {} After: {}'.format(before.guild.name, before.name, before.raw_status, after.raw_status))
            garbage = 0
        # else:
            # all other updates, print out the member who changed
            # logger.info('[{}] {} - Some other update.'.format(before.guild.name, before.name))

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        logger.info('on_user_update: Guild: {} | [{}] {}'.format(before.guild.name, before.name, before.name))
        logger.info('on_user_update: Guild: {} | [{}] {}'.format(after.guild.name, after.name, after.name))

    @commands.Cog.listener()
    async def on_member_remove(self,member):
        logger.info('Member left: Guild: {} | {}'.format(member.guild.name, member))

# hold off on the .pending check until discord.py is updated to support the flag.
#    @commands.Cog.listener()
#    async def on_member_update(self,oldmember,newmember):
#        if (oldmember.pending == newmember.pending) :
#            logger.info('No pending change')
#        else:
#            logger.info('Old Member pending: {}'.format(oldmember.pending))
#            logger.info('New Member pending: {}'.format(newmember.pending))

def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(memberListener(bot))
# end of def setup

