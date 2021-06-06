import logging

from discord.ext import commands


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # every command needs owner permissions
    async def cog_check(self, ctx):
        #logger.info('cog_check: {}'.format(self.bot.owner_id == ctx.author.id))
        return self.bot.owner_id == ctx.author.id

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. Join the support discord server if you are having "
                           "any problems. This usage has been logged.")
            logger.warning(f'User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Current prefix is {}'.format(self.bot.command_prefix))
        else:
            logger.warning(error)
    # end of def cog_command_error

    @commands.command(aliases=['pre'])
    # @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, *, pre):
        """Set a custom prefix for the server."""
        server = ctx.message.guild
        if pre.endswith('\w'):
            pre = pre[:-2]+' '
            if len(pre.strip()) > 0:
                msg = f'The server prefix has been set to `{pre}` Use `{pre}prefix <prefix>` to change it again.'
            else:
                await ctx.send('Invalid prefix.')
                return
        else:
            msg = f'The server prefix has been set to `{pre}` Use `{pre}prefix <prefix>` to change it again. ' \
                  f'If you would like to add a trailing whitespace to the prefix, use `{pre}prefix {pre}\w`.'

        self.bot.command_prefix = str(pre)
        await ctx.send(msg)
    # end of def prefix

def setup(bot):
    # expose the logger in case there are errors in this module
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(Prefix(bot))
# end of def setup

