import logging
import discord
from datetime import datetime
from discord.ext import commands
import re
from unidecode import unidecode
from random import randint
import inspect


class nick(commands.Cog, command_attrs=dict(hidden=True)):
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
            wronguser = wronguser[6:]
            await ctx.send('Member \"{}\" not found.'.format(wronguser))
        else:
            logger.warning('nick cog error: {}'.format(error))
    # end of def cog_command_error


    #
    # nickHelp : display help
    #
    async def nickHelp(self, ctx):
        embedtitle = f'Changing a member\'s nickname:'
        embeddesc  = f'`.nick @member new nickname [INIT]`'
        embeddesc += f'\n\nYou can use a discord @mention just like you were mentioning someone.  For example:\n'
        embeddesc += f'`.nick @khan#1819 K4HN [FLRK]`\n'
        embeddesc += f'\nNote: You cannot change the nickname of someone who has higher permissions than you have.'

        embed = discord.Embed(title=embedtitle, colour=discord.Colour(0xaf000), description=embeddesc)

        embed.set_author(name=self.bot.mafdetlist[randint(0,len(self.bot.mafdetlist))], icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
    # end of nickHelp


    #
    # nick : change the nickname of a member
    #
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, newnick=None):
        # if no parameters were entered for this command, then the cog_command_error will handle this 
        # with a MissingRequiredArgument exception
        logger.info('nick:   {} top_role: {}/{}'.format(ctx.message.guild.me, ctx.message.guild.me.top_role, ctx.message.guild.me.top_role.position))
        logger.info('nick:   {} top_role: {}/{}'.format(member.display_name, member.top_role, member.top_role.position))
        logger.info('nick:   {} top_role: {}/{}'.format(ctx.author.display_name, ctx.author.top_role, ctx.author.top_role.position))

        # 1. the bot must have >= permissions than the person being changed otherwise an error will happen
        if ctx.message.guild.me.top_role < member.top_role:
            logger.warning('nick: server config error - bot is not high enough to change nickname')
            await ctx.send('Server error: The bot does not have permission to change the nicknames of people with the {} role.'.format(member.top_role))
            return
        else:
            logger.info('nick: bot perms OK.')

        # 2. the person using the nick command must have a higher role than the person being changed.
        if ctx.author.top_role < member.top_role:
            logger.info('nick: user does not have high enough permissions to change {}'.format(member.displa_name))
            await ctx.send('You cannot change the nickname of anyone who has higher permissions than you have.')
            return
        else:
            logger.info('nick: {} >= {}'.format(ctx.author.display_name,member.display_name))

        if newnick == None:
            # display help
            logger.info('nick: newnick is none')
            await ctx.send('You forgot to enter the new nickname.')
            await self.nickHelp(ctx)
            return
        elif newnick.lower == 'help':
            logger.info('nick: user said help')
            await self.nickHelp(ctx)
            return
        elif newnick.lower == 'none':
            logger.info('nick: removing nickname')
            newnick = None
        # endif 
        
        logger.info('nick new nickname: {}'.format(newnick))

        try:
            # newnick should be in the format <name> [alliance]
            oldName = member.display_name
            memberID = member.id
            await member.edit(nick=newnick)
            # fetch the info from the server after updating
            newmember = await ctx.guild.fetch_member(memberID)
            logger.info('nick newmember: {}'.format(newmember))
            # await ctx.send('{} is now {}'.format(oldName,newmember.nick))

            if newmember.nick == None:
                nick_wo_accents = "None"
            else:
                nick_wo_accents = unidecode(newmember.nick)

            embed = discord.Embed()
            embed.add_field(name="User",value=newmember.name, inline=True)
            embed.add_field(name="New Nickname",value=newmember.nick, inline=True)
            embed.add_field(name="w/o diacritics",value=nick_wo_accents, inline=True)
            #embed.add_field(name="Top Role",value=newmember.top_role, inline=False)
    
            await ctx.send('Nickname changed:',embed=embed)

        except Exception as err:
            logger.warning('nick: unknown error: {}'.format(err))
            logger.warning('nick: {} top_role: {}'.format(ctx.author.display_name, ctx.author.top_role))
            logger.warning('nick: {} top_role: {}'.format(member.display_name, member.top_role))
        return
    # end of nick
    '''
    # nick error handler
    @nick.error
    async def nickError(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            # we were expecting a user to be entered.  If we get a 
            # MissingRequiredArgument error, then the user didn't enter a member
            logger.info('nickError MRA: {}'.format(error))
            await ctx.send('Member {} not found.'.format(member))
            await self.nickHelp(ctx)
        elif isinstance(error, commands.BadArgument):
            # we were expecting a user to be entered.  If we get a 
            # BadArgument(member) error, then the member wasn't found.
            logger.info('nickError: BadArgument. parm entered is not a member.')
        else:
            logger.info('nickError: {}'.format(error))
    '''

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(nick(bot))
# end of def setup

