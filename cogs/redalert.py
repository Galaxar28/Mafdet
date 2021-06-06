import logging
import discord
import asyncio
import datetime
import pytz
import re
from random import randint
from discord.ext import commands


class redAlert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # the red alert channel MUST be named "red-alert"
        # on the test server, the red alert channel id = 604790682753695745

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


    async def send_embed(self, ctx, coords, rachannel, ratext):
        # create the embed
        if ratext == '':
            embed = discord.Embed(title="**RED ALERT**", colour=discord.Colour(0xaf0000))
        else:
            embed = discord.Embed(title="**RED ALERT**", colour=discord.Colour(0xaf0000), description=ratext)

        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/memoryalpha/images/6/6b/RedAlert.jpg/revision/latest?cb=20100117050244&path-prefix=en")
        embed.set_author(name=ctx.author.display_name + " says", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Coordinates", value=coords, inline=False)

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
            if ctx.channel.name != rachannel.name:
                await ctx.send("The red alert will be posted in #red-alert for 10 minutes.", embed=embed)
                # send the coordinates as a regular message to make it easy to copy/paste into the game.
                # Embed's can't be copied on phones/tablets
                await ctx.send(coords)
                logger.info('Red Alert: posted coords to ctx channel')
        except Exception as error:
            logger.warning('Red Alert: Error sending a message: {}'.format(error))

        try:
            await rachannel.send(embed=embed, delete_after=60*10)
            # send the coordinates as a regular message to make it easy to copy/paste into the game.
            # Embed's can't be copied on phones/tablets
            await rachannel.send(coords, delete_after=60*10)
            logger.info('Red Alert: posted coords to red alert channel')
        except Exception as error:
            logger.warning('Red Alert: Error sending to red alert channel: {}'.format(error))

        logger.info('Red Alert: ({}) {} {}'.format(ctx.author.display_name, coords, ratext))
    # end of send_embed

    @commands.command()
    # @commands.has_role('redalertcreate')
    # could also use @commands.has_any_role("redalertcreate", 'role2', 'role3'...)
    # @commands.has_permissions(manage_guild=True)
    async def redalert(self, ctx, *, allargs=None):
        """Send a Red Alert message to the #dashboard channel"""
        coords = ''
        ratext = ''
        if allargs != None:
            logger.info('redalert args: {}'.format(allargs))
        else:
            logger.info('redalert (no args)')

        if allargs == None or allargs == "help":
            embedtitle = f'How to raise a RED ALERT'

            embeddesc  = f'Red alerts are great to notify others of an attack by a hostile, '
            embeddesc += f'coordinating an attack on an enemy, or anything happing in-game that '
            embeddesc += f'won\'t matter after 10 minutes.\n'
            embeddesc += f'Enter all the red alert information on one line like this:'

            embed = discord.Embed(title=embedtitle, colour=discord.Colour(0xaf0000), description=embeddesc)

            embed.set_author(name=self.bot.mafdetlist[randint(0,len(self.bot.mafdetlist)-1)], icon_url=self.bot.user.avatar_url)
            embed.add_field(name="`.redalert [System Space S:23445 X:4.2342 Y:-23.23422] Help me! My base is getting attacked!`", 
                            value="Contact Galaxar if you have questions.", inline = False)
            await ctx.send(embed=embed)
            return
        # end of if allargs == help

        # parse allargs to see if we have the right info for a redalert.
        # if not, give a useful error message to the user
        #
        # Format changes depending on the reference (open space, planet, etc.) 
        #   player without alliance, in same system
        #     [player name no alliance X:-342 Y:34] 
        #   player with alliance, in same system
        #     [[init] player name X:-234 Y:-342] 
        #   systems always have "System" in the coordinates
        #     [system name System S:23421] 
        #   places in space have "Space" in the coordinates
        #     [system Space S:23445 X:4.234233 Y:-23.23422] 
        #   planet where bases can relocate
        #     [Station Housing planet name S:12345 X:-234.23 Y:234.23424] 
        #   "thing" in open space
        #     [3★ Raw Gas Mine S:1379808121 X:677.123 Y:167] 
        #   player with alliance in different system]
        #     [[FŁRK] Maddkelt S:1911521293 X:191.2568 Y:-367.3874] 
        #   generalized format
        #     [<object name> S:<system number> X:<+/- x.x coordinate> Y:<+/- y.y coordinate>]
        #     where <object name> can be
        #     [text] or [[inits] text]

        searchPattern = re.compile('(\[.*\])(\s*)(.*)')
        # group 1 = coordinates
        # group 2 = space(s) between group 1 and 3
        # group 3 = red alert message
        if searchPattern.search(allargs):
            coords = searchPattern.search(allargs).group(1)
            ratext = searchPattern.search(allargs).group(3)
        else:
            await ctx.send("Usage: .redalert [coordinates] <optional message>\n"
                     "For example:\n"
                     "`.redalert [3★ Raw Gas Mine S:1379808121 X:677.123 Y:167] JT is camped at a gas mine!`")
            return
        # end of if searchPattern...

        logger.info('redalert coords: {}'.format(coords))
        logger.info('redalert ratext: {}'.format(ratext))

        # find the red alert channel
        rachannel = discord.utils.get(ctx.guild.text_channels, name='red-alert')
        logger.info('rachannel: {}'.format(rachannel))
        if rachannel == None:
            await ctx.send("Sorry, the red-alert channel is not setup.")
            return
        try:
            await self.send_embed(ctx, coords, rachannel, ratext)
            logger.info('Red Alert: sent embed')
        except Exception as err:
            logger.warning(err)
        # if we need to delete multiple messages (like the old_redalert), then use
        # await ctx.message.delete_messages(<list of messages>)
        await ctx.message.delete()

    # end of redalert


def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(redAlert(bot))
# end of def setup

