import logging
import discord
from datetime import datetime
from discord.ext import commands
import re
from unidecode import unidecode

#
# newshow - display info about users, roles, channels, alliances
#
class NewShowMe(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    # every command needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id

    # cog error handler
    async def cog_command_error(self, ctx, error):
        logger.info('newshow: invoked subcommand is {}'.format(ctx.invoked_subcommand))
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. Join the support discord server if "
                           "you are having any problems. This usage has been logged.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Usage: .newshow <searchtype> <searchterm>')
        else:
            logger.warning(error)
    # end of def cog_command_error


    #
    # sendTheMsg - Send the message to the right destination
    #
    async def sendTheMsg(self, ctx, rt, msgembed):
        logger.info('inside sendTheMsg')
        await ctx.send('inside send the msg')
        # if the command was issued on the test server, just send the embed back to the channel.
        # otherwise send a DM to the user
        if ctx.guild.id == 568662023970488320: # JustATestServer
        # if ctx.guild.id == 533820631435837440: # Coalition Server
        # if ctx.guild.id in [568662023970488320, 533820631435837440] :
            logger.info('newshow: using test server')
            try:
                await ctx.send(rt, embed=msgembed)
            except Exception as err:
                logger.warning(err)
                raise err
        else:
            logger.info('newshow: using DM')
            try:
                await ctx.author.send(rt, embed=msgembed)
            except Exception as err:
                logger.warning(err)
                raise err
    # end of sendTheMsg


    #
    # NEWSHOW Group
    #
    @commands.group()
    async def newshow(self, ctx):
        """Usage: show <search type> <search term>
        where <search type> can be user | channel | role | alliance
              <search term> any text to search for
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No searchtype entered\n`Usage: .newshow <searchtype> <searchterm>\nValid search types are user, channel, role, alliance`')


    #
    # newshow subcommand : user
    #
    @newshow.command(name='user')
    async def _user(self, ctx, member: discord.Member):
        try:
            await ctx.send('{0.display_name} joined on {0.joined_at}'.format(member))
            embed = discord.Embed()
            logger.info('newshow: found user')
            embed.add_field(name="Display Name",value=member.display_name, inline=True)
            embed.add_field(name="Nickname",value=member.nick, inline=True)
            embed.add_field(name="ASCII",value=unidecode(member.nick), inline=True)
            embed.add_field(name="Top Role",value=member.top_role, inline=False)
            # embed.add_field(name="ID",value=member.id, inline=False)

            rolelist= []
            sortedrolelist = ""
            for r in member.roles:
               if r.name != "@everyone":
                   rolelist.append(r.name)
            sortedrolelist = sorted(rolelist)
                   # rolelist += r.name + "\n"
            embed.add_field(name="Assigned Roles", value=sortedrolelist, inline=False)
            embed.add_field(name="Joined this server (US Eastern Time)",
                            value=member.joined_at.strftime("%a, %b %d, %Y at %-I:%M:%S %p"), inline=True)
            embed.add_field(name="Joined Discord (US Eastern Time)",
                            value=member.created_at.strftime("%a, %b %d, %Y at %-I:%M:%S %p"), inline=True)
            # embed.add_field(name="Permissions",value=member.guild_permissions.value,inline=False)
            # no text needed to return
            logger.info('ready to send')
            message = '    Found: {}'.format(member.display_name)
            await ctx.send(message)
            await self.sendTheMsg(ctx, message, embed)
            logger.info('sent?')
        except Exception as err:
            logger.warning(err)
        return
    # end of _user

    @_user.error
    async def _user_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            logger.info('newshow user: user input error')
        elif isinstance(error, commands.MissingRequiredArgument):
            logger.info('newshow user: missing required argument')
        elif isinstance(error, commands.BadArgument):
            # we were expecting a user to be entered.  If we get a
            # BadArgument error, then the member wasn't found.
            await ctx.send('Member {} not found.'.format(member))
        else:
            logger.info('newshow user: {}'.format(error))
        return
    # end of _user_error


    #
    # newshow subcommand : role
    #
    @newshow.command(name='role')
    async def _role(self, ctx, role: discord.Role):
        try:
            logger.info('looking up role: {}'.format(role.name))
            embed = discord.Embed()
            embed.add_field(name="Totem Pole Position: {}".format(role.position),value="Permissions: {}".format(bin(role.permissions.value)))

            #        12345678901234567890
            f1  = f'`Is admin        : {role.permissions.administrator}`\n'
            f1 += f'`Create invites  : {role.permissions.create_instant_invite}`\n'
            f1 += f'`Kick members    : {role.permissions.kick_members}`\n'
            f1 += f'`Ban members     : {role.permissions.ban_members}`\n'
            f1 += f'`Manage channels : {role.permissions.manage_channels}`\n'
            f1 += f'`Read messages   : {role.permissions.read_messages}`\n'
            f1 += f'`Read history    : {role.permissions.read_message_history}`\n'
            f1 += f'`Send messages   : {role.permissions.send_messages}`\n'
            f1 += f'`Manage nicknames: {role.permissions.manage_nicknames}`\n'

            p = re.compile('(False)')
            f1 = p.sub('N', f1)
            p = re.compile('(True)')
            f1 = p.sub('Y', f1)

            logger.info('len of role_info embed: {}'.format(len(f1)))
            embed.add_field(name=f1, value='-', inline=False)

            message = '    Found role: {}'.format(role.name)
            await self.sendTheMsg(ctx, message, embed)
            guild = role.guild

            memberlist = []
            for memb in guild.members:
                if role in memb.roles:
                    addtolist = f'{memb.display_name} (aka {memb.name})'
                    memberlist.append(addtolist)
            memberlist.sort(key=str.lower)
            returntext = "Members who have this role:"
            for m in memberlist:
                returntext += "\n" + m
            await ctx.send(returntext)
        except Exception as err:
            logger.warning('newshow role: {}'.format(err))
        # end of try
        return
    # end of _role

    @_role.error
    async def _role_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            logger.info('newshow role: user input error')
        elif isinstance(error, commands.MissingRequiredArgument):
            logger.info('newshow role: missing required argument')
        elif isinstance(error, commands.BadArgument):
            # we were expecting a role to be entered.  If we get a
            # BadArgument error, then the member wasn't found.
            await ctx.send('Role {} not found.'.format(member))
        else:
            logger.info('newshow role: {}'.format(error))
        return
    # end of _role_error


    #
    # Channel Info - called from NEWSHOW
    #
    @newshow.command(name='channel')
    async def _channel(self, ctx, channel):
        logger.info('newshow: searching for channel')
        # first, check to see if this is a valid channel
        if channel == '':
            await ctx.send('No channel specified.')
            return
        else:
            logger.info('searching for channel {}'.format(channel))

        channel_found = None
        for channel_search in ctx.guild.channels:
            if channel_search.name == channel:
                logger.info('found a channel.')
                channel_found = channel_search
        if channel_found == None:
            logger.info('channel not found')
            return
        else:
            logger.info('channel found')

        try:
            f1 = ''
            logger.info('category_id: {}'.format(channel_found.category_id))
            category = ctx.guild.get_channel(channel_found.category_id)
            logger.info('category: {}'.format(category))
            if category:
                categoryname = category.name
                logger.info('category name: {}'.format(categoryname))
                #        12345678901234567890
                f1  = f'`Category        : {categoryname}`\n'
            # end of categoryobj

            #        12345678901234567890
            f1 += f'`Channel topic   : {channel_found.topic}`\n'

            p = re.compile('(False)')
            f1 = p.sub('N', f1)
            p = re.compile('(True)')
            f1 = p.sub('Y', f1)

            logger.info('len of channel_info embed: {}'.format(len(f1)))
            embed = discord.Embed()
            message = '    Found: {}'.format(channel_found.name)
            embed.add_field(name=f1, value='-', inline=False)
            await self.sendTheMsg(ctx, message, embed)

            memberlist = []
            for memb in channel.members:
                mydata = discord.utils.find(lambda m: m.name == memb, ctx.channel.guild.members)
                if memb.display_name != memb.name:
                    addtolist = memb.display_name + "  (aka " + memb.name + ")"
                else:
                    addtolist = memb.display_name
                memberlist.append(addtolist)
            memberlist.sort(key=str.lower)
            returntext = "Members who can see this channel:\n"
            for m in memberlist:
                returntext += m + "\n"
            await ctx.send(returntext)
        except Exception as err:
            logger.warning('newshow channel: {}'.format(err))
        # end of try
        return
    # end of _channel

    @_channel.error
    async def _channel_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            logger.info('newshow channel: user input error')
        elif isinstance(error, commands.MissingRequiredArgument):
            logger.info('newshow channel: missing required argument')
        elif isinstance(error, commands.BadArgument):
            # we were expecting a channel to be entered.  If we get a
            # BadArgument error, then the channel wasn't found.
            await ctx.send('Channel {} not found.'.format(member))
        else:
            logger.info('newshow channel: {}'.format(error))
        return
    # end of _role_error



    '''
    #
    # Alliance Info - called from SHOWME
    #
    def alliance_info(self, ctx, embed, channelobj):
        logger.info('showme: found text channel')


    #
    # SHOWME Command
    #
    @commands.command()
    async def showme(self, ctx, *, searchterm=None):
        """Show information about members, aliances, roles, etc."""
        # delete the command -- don't have to show who's looking up what.
        # Send the results of the search in a DM to the user.
        try:
            # ctx.message.delete

            if searchterm is None:
                await ctx.send('Usage: .showme <one word to search the server>')
                return

            logger.info('showme: searching for: {}'.format(searchterm))

            # build a nice embed to display the info
            embed = discord.Embed()
            returnText = 'Search term: {}'.format(searchterm)

            # start with finding info about a user
            try:
                mydata = discord.utils.find(lambda m: m.display_name == searchterm, ctx.channel.guild.members)
            except Exception as err:
                logger.info('showme: found user - exception')
                raise err
            if mydata:
                # found a member
                logger.info('showme: found a member')
                (mytext, embed) = self.user_info(ctx, embed, mydata)
                if mytext:
                    returnText += mytext
                await self.sendTheMsg(ctx, returnText, embed)
                return
            else:
                logger.info('showme: not a member')
            # end of trying to find a user

            # if the search did not find a user, try finding a role
            try:
                mydata = discord.utils.find(lambda r: r.name == searchterm, ctx.message.guild.roles)
            except Exception as err:
                logger.info('showme: found role - exception')
                raise err
            if mydata:
                # found a role
                logger.info('showme: found a role')
                (mytext, embed) = self.role_info(ctx, embed, mydata)
                if mytext:
                    returnText += mytext
                await self.sendTheMsg(ctx, returnText, embed)
                return
            else:
                logger.info('showme: not a role')
            # end of trying to find a role

            # if the search did not find a role, try finding a channel
            try:
                mydata = discord.utils.find(lambda r: r.name == searchterm, ctx.message.guild.channels)
            except Exception as err:
                logger.info('showme: found channel - exception')
                raise err
            if mydata:
                # found a channel
                logger.info('showme: found a channel')
                try:
                    (mytext, embed) = self.channel_info(ctx, embed, mydata)
                except Exception as err:
                    logger.info('showme: error with channel_info line')
                    raise err
                logger.info('after channel_info')
                if mytext:
                    returnText += mytext
                await self.sendTheMsg(ctx, returnText, embed)
                return
            else:
                logger.info('showme: not a role')
            # end of trying to find a channel

            # if we're here, then the search came up empty.
            # send the user a message that their search turned up empty and delete
            # both messages after 15 seconds.
            await ctx.send('showme: search for \"{}\" not found'.format(searchterm), delete_after=15)
            await ctx.message.delete(delay=15)
        except Exception as err:
            logger.warning("showme encountered an unknown error")
            raise err
    # end of showme

    @commands.command()
    async def showinvites(self, ctx, *, chname=''):
        chlist = []
        if chname == '':
            for x in ctx.guild.channels:
                chlist.append(x.name)
        else:
            chlist.append(chname)
        mylist = ''
        try:
            for chnlname in chlist:
                channelobj = discord.utils.find(lambda r: r.name == chnlname, ctx.message.guild.channels)
                if isinstance(channelobj, discord.CategoryChannel):
                    continue
                mylistofinvites = await channelobj.invites()
                if mylistofinvites:
                    for myinvite in mylistofinvites:
                        mylist += myinvite.inviter.display_name + ' created invite: `' + myinvite.code + '` for ' + myinvite.channel.mention + ' on ' + myinvite.created_at.strftime("%a, %b %d, %Y") + '\n'
        except Exception as err:
            logger.warning(err)
            raise err

        if mylist > '' :
            await ctx.send(mylist)
        else:
            await ctx.send('No invites for {}'.format(chname))
    # end of showinvites
    '''
def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(NewShowMe(bot))
# end of def setup

