import logging
import discord
from discord.ext import commands


class addRA(commands.Cog, command_attrs=dict(hidden=True)):
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

    @commands.command(hidden=True)
    # @commands.has_permissions(manage_guild=True)
    async def addra(self, ctx):
        memberrole = discord.utils.get(ctx.guild.roles, name="Coalition members")
        logger.info('membership: {}'.format(memberrole))
        rarole = discord.utils.get(ctx.guild.roles, name="redalertread")
        logger.info('rarole: {}'.format(rarole))
        for member in ctx.guild.members:
            logger.info('member: {}'.format(member.display_name))
            #logger.info('member {} roles: {}'.format(member.display_name,member.roles))
            if memberrole in member.roles:
                logger.info('Member in membership: {}'.format(member.display_name))
                try:
                    await member.add_roles(rarole)
                except Exception as err:
                    logger.warning(err)
            else:
                logger.info('not a member')
    # end of addra

    '''
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
    '''


def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(addRA(bot))
# end of def setup

