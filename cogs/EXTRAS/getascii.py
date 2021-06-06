import logging
import re
from confusables import Confusables
import discord
from discord.ext import commands

class convert_to_ASCII():
    def __init__(self, bot):
        self.bot = bot

        """
        Parse confusables file into a dict of arrays.
        """
        confusables_dict = defaultdict(list)
        pattern = re.compile(r'(.) → (.)')
        with open('confusables.txt', 'r') as f:
            for line in f:
                r = pattern.search(line)
                if r:
                    fake = r.group(1)
                    auth = r.group(2)
                    confusables_dict[auth].append(fake)
            self.confusables_dict = confusables_dict
        # dict is loaded with confusables_dict[real]



    def getASCII(string : inputstring):
	    c = Confusables('confusables.txt')
	    cpattern = c.confusables_regex(inputstring)
		r = re.compile(cpattern)

    @commands.command()
    async def cooltest(self, ctx):
        """test"""
        await ctx.send('this is a test.')

    @commands.group()
    async def cool(self, ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('No, {0.subcommand_passed} is not cool'.format(ctx))
    
    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        await ctx.send('Yes, the bot is cool.')
    
    @cool.command(name='user')
    async def _user(self, ctx, name=None):
        """Is the user cool?"""
        if name:
            await ctx.send('Yes, {} is cool.'.format(name))
        else:
            await ctx.send('Usage: .cool user <user name>')
    
def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(convert_to_ASCII(bot))
# end of setup

