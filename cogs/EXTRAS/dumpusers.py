import logging
import discord
from datetime import datetime
from discord.ext import commands
import re
from unidecode import unidecode

class dumpUsers(commands.Cog, command_attrs=dict(hidden=True)):
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
            await ctx.send("Only the owner can use this module.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) tried to use a dumpUsers command')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('missing arg')
        else:
            logger.warning(error)
    # end of def cog_command_error


    def getmr(self, ctx, member: discord.Member):
        try:
            mR = []
            mR.append(member.display_name)
            mR.append(member.nick)
            if member.nick:
                asciinick = unidecode(member.nick)
                mR.append(asciinick)
                searchPattern = re.compile('\[(.*)\]')
                # group 1 = alliance
                try:
                    alliance = searchPattern.search(asciinick).group(1)
                    mR.append(alliance)
                except Exception as error:
                    logger.info('member: {}: {}'.format(member.display_name, error))
                    mR.append('none')
            else:
                mR.append('none') # no nickname
                mR.append('none') # no alliance




            mR.append(member.top_role)
            mR.append(member.name+"#"+member.discriminator)
            mR.append(member.joined_at.strftime("%a, %b %d, %Y at %-I:%M:%S %p"))
            mR.append(member.created_at.strftime("%a, %b %d, %Y at %-I:%M:%S %p"))
            mR.append(member.id)
            mR.append(member.guild_permissions.value)
            rolelist= [] 
            sortedrolelist = ""
            for r in member.roles:
               if r.name != "@everyone":
                   rolelist.append(r.name)
            sortedrolelist = sorted(rolelist)
            rl = ""
            for x in sortedrolelist:
                #rl += x + "	" # tab
                rl += x + "\t" # tab
            mR.append(rl)
        except Exception as err:
            logger.warning(err)
        return mR 
    # end of getmr


    @commands.command(hidden=True)
    async def getonemr(self, ctx, member: discord.Member):
        memberRecord = []
        try:
            fname = ctx.guild.name + '_member_records.txt'
            fname = re.sub(" ", "_", fname)
            with open(fname, 'a') as f:
                header = "display_name\tnick\tnick w/o diacritics\talliance\ttop_role\tname#discriminator\tjoined_at\tcreated_at\tid\tguild_permissiona\tall_roles\n"
                #header = "display_name	nick	nick w/o diacritics	alliance	top_role	name#discriminator	joined_at	created_at	id	guild_permissiona	all_roles\n"
                f.write(header)
                f.write(fname + "\n")
            memberRecord = self.getmr(ctx, member)
            line = ""
            for item in memberRecord:
                #line += str(item) + "	" # tab
                line += str(item) + "\t" # tab
            line += "\n"
            with open(fname, 'a') as f:
                f.write(line)
        except Exception as error:
            logger.info(error)
        await ctx.send('Done.')
    # end of getonemr

    @commands.command(hidden=True)
    async def getallmr(self, ctx):
        try:
            fname = ctx.guild.name + '_member_records.txt'
            fname = re.sub(" ", "_", fname)
            with open(fname, 'a') as f:
                header = "display_name\tnick\tnick w/o diacritics\talliance\ttop_role\tname#discriminator\tjoined_at\tcreated_at\tid\tguild_permissiona\tall_roles\n"
                #header = "display_name	nick	nick w/o diacritics	alliance	top_role	name#discriminator	joined_at	created_at	id	guild_permissiona	all_roles\n"
                f.write(header)
                f.write(fname + "\n")
            for member in ctx.guild.members:
                memberRecord = self.getmr(ctx, member)
                line = ""
                for item in memberRecord:
                    #line += str(item) + "	" # tab
                    line += str(item) + "\t" # tab
                line += "\n"
                with open(fname, 'a') as f:
                    f.write(line)
        except Exception as err:
            logger.info(err)
        await ctx.send('Done.')
    # end of getallmr

    '''
    async def user_info(self, ctx, embed, userobj):
    # end of user_info


    #
    # Role Info - called from SHOWME
    #
    def role_info(self, ctx, embed, roleobj):
        logger.info('showme: found role')
        try:
            #        12345678901234567890
            f1  = f'`Is admin        : {roleobj.permissions.administrator}`\n'
            f1 += f'`Create invites  : {roleobj.permissions.create_instant_invite}`\n'
            f1 += f'`Kick members    : {roleobj.permissions.kick_members}`\n'
            f1 += f'`Ban members     : {roleobj.permissions.ban_members}`\n'
            f1 += f'`Manage channels : {roleobj.permissions.manage_channels}`\n'
            f1 += f'`Read messages   : {roleobj.permissions.read_messages}`\n'
            f1 += f'`Read history    : {roleobj.permissions.read_message_history}`\n'
            f1 += f'`Send messages   : {roleobj.permissions.send_messages}`\n'
            f1 += f'`Manage nicknames: {roleobj.permissions.manage_nicknames}`\n'

            p = re.compile('(False)')
            f1 = p.sub('N', f1)
            p = re.compile('(True)')
            f1 = p.sub('Y', f1)

            logger.info('len of role_info embed: {}'.format(len(f1)))

            embed.add_field(name=f1, value='-', inline=False)
        except Exception as err:
            logger.warning(err)
            raise err
        return f'    Found: Role', embed
    # end of role_info


    #
    # Channel Info - called from SHOWME
    #
    def channel_info(self, ctx, embed, channelobj):
        logger.info('showme: found text channel')
        try:
            f1 = ''
            logger.info('category_id: {}'.format(channelobj.category_id))
            categoryobj = ctx.guild.get_channel(channelobj.category_id)
            logger.info('categoryobj: {}'.format(categoryobj))
            if categoryobj:
                categoryname = categoryobj.name
                logger.info('category name: {}'.format(categoryname))
                #        12345678901234567890
                f1  = f'`Category        : {categoryname}`\n'
            # end of categoryobj

            #        12345678901234567890
            f1 += f'`Channel topic   : {channelobj.topic}`\n'

            p = re.compile('(False)')
            f1 = p.sub('N', f1)
            p = re.compile('(True)')
            f1 = p.sub('Y', f1)

            logger.info('len of role_info embed: {}'.format(len(f1)))

            embed.add_field(name=f1, value='-', inline=False)

            memberlist = []
            for memb in channelobj.members:
                # mydata = discord.utils.find(lambda m: m.name == memb, ctx.channel.guild.members)
                if memb.display_name != memb.name:
                    addtolist = memb.display_name + "  (aka " + memb.name + ")"
                else:
                    addtolist = memb.display_name
                memberlist.append(addtolist)
            memberlist.sort(key=str.lower)
            returntext = "Members who can see this channel:\n"
            for m in memberlist:
                returntext += m + "\n"
        except Exception as err:
            logger.warning(err)
            raise err
        return f'    Found: Text Channel\n'+returntext, embed


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
    bot.add_cog(dumpUsers(bot))
# end of def setup

