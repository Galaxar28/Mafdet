import logging
import discord
import asyncio
import datetime
import pytz
import re
from discord.ext import commands


# define custom exception
class InTheMiddle(Exception):
    """Raised when a command is entered in the middle of executing another command"""
    pass

class old_redAlert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # red alert channel id = 604790682753695745

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You do not have sufficient rank to raise a red alert!")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send('You can not use the redalert command in a DM')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. This usage has been logged.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('need to do something here?  Missing Required Argument')
        else:
            logger.warning("unknown error: {}".format(error))
    # end of def cog_command_error


    @commands.command()
    @commands.has_role('redalertcreate')
    # could also use @commands.has_any_role("redalertcreate", 'role2', 'role3'...)
    # @commands.has_permissions(manage_guild=True)
    async def old_redalert(self, ctx):
        """Send a Red Alert message
        to the #dashboard channel (auto deletes in 10 minutes)"""

        # find the red alert channel
        rachannel = discord.utils.get(ctx.guild.text_channels, name='red-alert')
        logger.info('rachannel: {}'.format(rachannel))
        if rachannel == None:
            await ctx.send("Sorry, the red-alert channel is not setup.")
            return

        # clean_up deletes the interim messages of the red alert creation
        async def clean_up(ml):
            logger.info('{} messages to delete'.format(len(ml)))
            try:
                await ctx.channel.delete_messages(ml)
            except Exception as err:
                logger.warning('Error deleting {} messages: {}'.format(len(ml),err))

        # define a check for the wait_for so that we keep waiting until 
        # the right user replies in the correct channel
        # and that the user didn't try to start a new command
        def check(m):
            try:
                logger.info('m.author / ctx.author {} / {}'.format(m.author,ctx.author))
                logger.info('m.channel / ctx.message.channel {} / {}'.format(m.channel,ctx.message.channel))
                logger.info('bot prefix: {}'.format(self.bot.command_prefix))
                # return m.author == ctx.author and m.channel == ctx.message.channel and not m.content.startswith(".")
                return m.author == ctx.author and m.channel == ctx.message.channel
            except Exception as err:
                logger.warning('check err: {}'.format(err))

        # create list of messages to delete when the command completes
        message_list = []

        # add the command to the list
        message_list.append(ctx.message)

        # Get the coordinates
        try:
            message_list.append(await ctx.send("Where is the Red Alert (enter the coordinates)?\nEnter \'stop\' to cancel the command."))
            coords = await self.bot.wait_for('message', timeout=20, check=check)
            message_list.append(coords)
            if coords.content.startswith(self.bot.command_prefix):
                logger.info('User entered a command in the middle of a command.')
                await ctx.send("You cannot enter a command in the middle of another command.\n.redalert command cancelled")
                await clean_up(message_list)
                return
        except asyncio.TimeoutError:
            logger.info('timed out getting coordinates')
            await clean_up(message_list)
            await ctx.send("Red Alert command cancelled (timed out)")
            return
        except Exception as err:
            logger.warning('Error getting coords: {}'.format(err))
            return

        # if the user wants to stop the command:
        logger.info('msg: {}'.format(coords.content))
        if coords.content == 'stop':
            logger.info('user stopped the redalert')
            await clean_up(message_list)
            try:
                await ctx.send('redalert command cancelled.')
            except Exception as err:
                logger.warning(err)
            return

        # Get a message to include with the red alert
        mytxt  = "What message or other info do you want to include in the Red Alert notification?\n"
        mytxt += "Enter the word \'none\' if you don\'t want to include separate message."
        mytxt += "\nEnter \'stop\' to cancel the command."
        try:
            message_list.append(await ctx.send(mytxt))
            ratext = await self.bot.wait_for('message', timeout=30, check=check)
            message_list.append(ratext)
            if ratext.content.startswith(self.bot.command_prefix):
                logger.info('User entered a command in the middle of a command.')
                await ctx.send("You cannot enter a command in the middle of another command.\n.redalert command cancelled")
                await clean_up(message_list)
                return
        except asyncio.TimeoutError:
            logger.info('timed out getting red alert text')
            await clean_up(message_list)
            await ctx.send("Red Alert command cancelled (timed out)")
            return
        except Exception as err:
            logger.warning('Error getting ratext: {}'.format(err))

        # if the user wants to stop the command:
        if ratext.content == 'stop':
            logger.info('user cancelled the redalert')
            await clean_up(message_list)
            await ctx.send('redalert command cancelled.')
            return

        # create the embed
        if ratext.content == 'none':
            embed = discord.Embed(title="**RED ALERT**", colour=discord.Colour(0xaf0000))
        else:
            embed = discord.Embed(title="**RED ALERT**", colour=discord.Colour(0xaf0000), description=ratext.content)

        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/memoryalpha/images/6/6b/RedAlert.jpg/revision/latest?cb=20100117050244&path-prefix=en")
        embed.set_author(name=ctx.author.display_name + " says", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Coordinates", value=coords.content, inline=False)

        # use pytz to convert all times to Eastern Time (USA)
        eastern = pytz.timezone('US/Eastern')
        raisedttm = datetime.datetime.now(eastern)
        canceldttm = raisedttm + datetime.timedelta(minutes = 10)

        # mytime = canceldttm.strftime("%a, %b %d, %Y at %-I:%M:%S %p US Eastern Time")
        mytime = canceldttm.strftime("%a, %b %d, %Y at %-I:%M:%S %p")
        logger.info('cancel time: {}'.format(mytime))
        embed.add_field(name="Red Alert expires at (US Eastern Time)", value=mytime, inline = False)
        # logger.info('embed built')

        try:
            await ctx.send("The red alert will be posted in #red-alert for 10 minutes.", embed=embed)
            # if the coordinates were entered in the right format, print them after the embed
            # to make it easy to copy/paste into the game.  Embed's can't be copied on
            # phones/tablets
            # new coords format as of Oct 2019:
            # [3★ Raw Gas Mine S:1379808121 X:677 Y:167]
            # if re.match('\[.*S:-?[0-9]+ X:-?[0-9]+[.0-9]* Y:-?[0-9]+[.0-9]*\]', coords.content.strip()):
            #if re.match('\[S:-*[0-9]+ X:-*[0-9]+\.[0-9]+ Y:-*[0-9]+\.[0-9]+\]', coords.content.strip()):
            if re.match('\[.*S:-?[0-9]+ X:-?[0-9]+[.0-9]* Y:-?[0-9]+[.0-9]*\]', coords.content.strip()):
                await ctx.send(coords.content)
                logger.info('Red Alert: posted coords to ctx channel')
        except Exception as error:
            logger.warning('Red Alert: Error sending a message: {}'.format(error))

        try:
            await rachannel.send(embed=embed, delete_after=60*10)
            # if the coordinates were entered in the right format, print them after the embed
            # to make it easy to copy/paste into the game.  Embed's can't be copied on
            # phones/tablets
            if re.match('\[.*S:-?[0-9]+ X:-?[0-9]+[.0-9]* Y:-?[0-9]+[.0-9]*\]', coords.content.strip()):
                await rachannel.send(coords.content, delete_after=60*10)
                logger.info('Red Alert: posted coords to red alert channel')
        except Exception as error:
            logger.warning('Red Alert: Error sending to red alert channel: {}'.format(error))

        logger.info('Red Alert: ({}) {} {}'.format(ctx.author.display_name, coords.content, ratext.content))

        # clean up interim messages
        await clean_up(message_list)

    # end of redalert


def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(old_redAlert(bot))
# end of def setup




