import logging
import discord
from datetime import datetime
from discord.ext import commands
import re
from unidecode import unidecode
from random import randint
import inspect


class nicktest(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    '''
    # every command needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id
    '''

    # cog error handler
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            logger.info('{} tried to use .nick but did not have permissions'.format(ctx.author.display_name))
            await ctx.send("You don't have permission to use the `{}` command.  Contact the admin for more info.".format(ctx.command))
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. Join the support discord server if "
                           "you are having any problems. This usage has been logged.")
            logger.warning(f'nick cog error: User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            # no parameters were entered at all.  Display the help
            logger.info('nickError MRA: {}'.format(error))

            await self.nickHelp(ctx)
        elif isinstance(error, commands.UserInputError):
            logger.info('nick cog error: user input error - bad member lookup?')
            # get what the user typed in
            logger.info('nick: UIE: {}'.format(ctx.message.clean_content))
            wronguser = ctx.message.clean_content
            wronguser = wronguser[9:]
            await ctx.send('Member \"{}\" not found.'.format(wronguser))
        else:
            logger.warning('nick cog error: {}'.format(error))
    # end of def cog_command_error


    #
    #
    # nickHelp : display help
    #
    async def nickHelp(self, ctx):
        embedtitle = f'Changing a member\'s nickname:'
        embeddesc  = f'`.nick @member new nickname [INIT]`\n'
        embeddesc += f'This command uses the discord @mention just like you were mentioning someone.  '
        embeddesc += f'For example:\n'
        embeddesc += f'`.nick @khan#1819 K4HN [FLRK]`'

        embed = discord.Embed(title=embedtitle, colour=discord.Colour(0xaf000), description=embeddesc)

        embed.set_author(name=self.bot.mafdetlist[randint(0,len(self.bot.mafdetlist))], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
    # end of nickHelp


    # nick 
    #
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nicktest(self, ctx, member: discord.Member, *, newnick=None):
        logger.info('nicktest self.bot: {}'.format(self.bot))
        logger.info('nicktest ctx.bot: {}'.format(ctx.bot))
        logger.info('nicktest ctx.message.guild.me.top_role: {}'.format(ctx.message.guild.me.top_role))
        logger.info('nicktest ctx.author.top_role: {}'.format(ctx.author.top_role))
        logger.info('nicktest member.top_role: {}'.format(member.top_role))
        logger.info('nicktest ctx.message.guild.me.top_role > ctx.author.top_role: {}'.format(ctx.message.guild.me.top_role > ctx.author.top_role))
        return
        try:
            doit = False
            logger.info('nicktest: online 101')
            if ctx.bot.me.top_role > ctx.author.top_role:
                logger.info('nicktest: permissions OK')
                doit = True
            elif ctx.bot.me.top_role < ctx.author.top_role:
                logger.info('nicktest: bot does not have higher permission')
            else:
                logger.info('nicktest: bot and member equal')
                doit = True
            if doit:
                await member.edit(nick=newnick)
            logger.info('nicktest: online 76')
        except Exception as err:
            logger.warning('unknown error: {}'.format(err))
        return
    # end of nicktest

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(nicktest(bot))
# end of def setup

