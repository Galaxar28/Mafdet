import logging
import discord
from discord.ext import commands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def listext(self, ctx):
        for myext in self.bot.extensions:
            logger.info(f"Ext: {myext}")

    @commands.command()
    async def listcog(self, ctx):
        for mycog in self.bot.cogs:
            logger.info(f"Cog: {mycog}")

    @commands.command()
    async def listcmd(self, ctx):
        logger.info('inside')
        cog = ctx.bot.get_cog('Info')
        commands = ctx.cog.get_commands()
        for c in commands:
            logger.info(f"{c.name}")
        for c in cog.walk_commands():
            logger.info(f"{c.qualified_name}")

    @commands.command()
    async def listlisteners(self, ctx):
        for name, func in ctx.cog.get_listeners():
            logger.info(f"{name} -> {func}")
           
def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(Info(bot))
# end of setup

