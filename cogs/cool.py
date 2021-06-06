import logging
import discord
from discord.ext import commands


class cool(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def cool(self, ctx):
        """Says if a user is cool.
        In reality this just checks if a subcommand is being invoked.
        """
        if ctx.invoked_subcommand is None:
            await ctx.send('Guild: {} | No, {0.subcommand_passed} is not cool'.format(self.guild.name, ctx))
    
    @cool.command(name='bot')
    async def _bot(self, ctx):
        """Is the bot cool?"""
        # await ctx.send('Yes, the bot is cool.')
        await ctx.send('Yes, {}, the bot is cool.'.format(ctx.author.mention))
    
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
    bot.add_cog(cool(bot))
# end of setup

