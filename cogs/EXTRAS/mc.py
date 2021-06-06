import logging
import discord
from discord.ext import commands


class merryChristmas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # every command needs owner permissions
    async def cog_check(self, ctx):
        # logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('need to do something here?  Missing Required Argument')
        else:
            logger.warning(error)
    # end of def cog_command_error

    @commands.command(hidden=True)
    # @commands.has_permissions(is_owner=True)
    async def mc(self, ctx):
        """Wishes everyone a Happy Hanukkah and a Merry Christmas"""
        try:
            pass
            await ctx.message.delete()
        except Exception as error:
            logger.warning('Error deleting posted message: {}'.format(error))
        try:
            # embed = discord.Embed(title="I hope everyone has a happy and safe Thanksgiving!",
            # colour=discord.Colour(0xaf0000), description='sample description goes here')

            embed = discord.Embed(
                        title="Merry Christmas and Happy Hanukkah!\n" +
                        "May this holiday season bring you peace and long life.",
                        colour=discord.Colour(0xaf0000))
            logger.info("1")
            # embed.set_thumbnail(url="https://i.ytimg.com/vi/Oy6mtBjQmW0/maxresdefault.jpg")
            embed.set_image(url="https://i.ytimg.com/vi/Oy6mtBjQmW0/maxresdefault.jpg")
            logger.info("2")

            embed.set_author(name="Mafdet", icon_url=self.bot.user.avatar_url)
            logger.info("3")

            await ctx.send(embed=embed)
            logger.info("4")

            logger.info('mafdet said, Merry Christmas')
        except Exception as error:
            logger.warning('Error sending a message: {}'.format(error))
    # end of setpresence


def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(merryChristmas(bot))
# end of def setup
