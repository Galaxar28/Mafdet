import logging

from discord.ext import commands

class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot

    # every command here needs owner permissions
    async def cog_check(self, ctx):
        logger.info('Guild: {} | cog_check: {}'.format(ctx.guild.name, self.bot.owner_id == ctx.author.id))
        logger.info(f'logger line - {self.bot.owner_id}')

        # logtext = (f'bot owner id: {self.bot.owner_id}')
        # logger.info('before logme call')
        # logme("info", ctx, logtext)
        # logger.info('after logme call')
        # logme("info", ctx, f'ctx author id: {ctx.author.id}')

        return self.bot.owner_id == ctx.author.id
    # end of def cog_check

    # cog error handler
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("Only the owner can use this module. Join the support discord server if you are having "
                           "any problems. This usage has been logged.")
            logger.warning(f'Guild: {ctx.guild.name} | User {ctx.author} ({ctx.author.id}) has tried to access a restricted '
                           f'command via {ctx.message.content}.')
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing a required argument for this command.")
        else:
            # logger.warning('Guild: {} | cog_command_error: {}'.format(ctx.guild.name, error))
            logger.warning('cog_command_error: {}'.format(error))
            raise error
    # end of def cog_command_error


    # unload a cog
    @commands.command(aliases=['u'])
    async def unload(self, ctx, *, cog):
        '''Unload an extension.'''
        logger.info(f'Guild: {ctx.guild.name} | Trying to unload cog: cogs.{cog}')
        reply = ' '
        try:
            self.bot.unload_extension('cogs.'+cog)
            logger.info('Guild: {} | unload_extension: {} unloaded'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" successfully unloaded.'
        except commands.ExtensionNotLoaded:
            logger.info('Guild: {} | unload_extension: {} is not loaded.'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" is not loaded.'
        except commands.ExtensionNotFound:
            logger.info('Guild: {} | unload_extension: {} is not found.'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" is not found.'
        except Exception as err:
            logger.inifo('Guild: {} | unload_extension: {} raised exception: {}'.format(ctx.guild.name, cog, err))
            reply = f'\nUnknown error unloading "cogs.{cog}".  Check logs.'
        # logger.info('Guild: {} | Reload command: {}'.format(ctx.guild.name, reply))
        await ctx.send(reply)
    # end of unload

    # reload command
    @commands.command(aliases=['r'])
    async def reload(self, ctx, *, cog):
        '''Reload an extension.'''
        #logme2("info", ctx, f'Trying to reload cog: {cog}')
        #logger.info(f'Guild: {ctx.guild.name} | Trying to reload cog: {cog}')
        #logger.info(f'Trying to reload cog: cogs.{cog}')

        reply = ''
        try:
            self.bot.reload_extension('cogs.'+cog)
            logger.info('Guild: {} | reload_extension: {} reloaded'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" successfully reloaded.'
        except commands.ExtensionNotFound:
            logger.warning('Guild {} | reload_extension: {} not found.'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" not found.'
        except commands.NoEntryPointError:
            logger.warning('Guild: {} | reload_extension: {} missing setup.'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" is missing a setup function.'
        #except commands.ExtensionFailed:
            # logger.warning('Guild: {} | reload_extension: {} failed to start.'.format(ctx.guild.name, cog))
            #reply = f'Cog: "cogs.{cog}" failed to start.'
        except commands.ExtensionNotLoaded:
            logger.info('Guild {} | reload_extension: {} is not loaded.'.format(ctx.guild.name, cog))
            reply = f'Cog: "cogs.{cog}" is not loaded... '
            try:
                reply += f'loading... '
                self.bot.load_extension('cogs.'+cog)
                logger.info('Guild: {} | load_extension: {} loaded.'.format(ctx.guild.name, cog))
                reply += f'loaded.'
            except commands.ExtensionAlreadyLoaded:
                logger.warning('Guild: {} | load_extension: {} already loaded.'.format(ctx.guild.name, cog))
                reply += f'\nCog (load_extension): Could not load or reload "cogs.{cog}" since it is already loaded.'
            except commands.ExtensionNotFound:
                logger.warning('Guild: {} | load_extension: {} not found'.format(ctx.guild.name, cog))
                reply += f'\nCog (load_extension): "cogs.{cog}" not found.'
            except commands.ExtensionFailed as err:
                logger.warning('Guild: {} | load_extension: {} failed to start.'.format(ctx.guild.name, cog))
                reply += f'\nCog (load_extension): "cogs.{cog}" failed to start: "{err}"'
            except Exception as err:
                logger.warning('Guild: {} | load_extension: {} raised exception: {}'.format(ctx.guild.name, cog, err))
                reply += f'\nUnknown error loading "cogs.{cog}".  Check logs.'
        except Exception as e:
            logger.warning('Guild: {} | reload_extension: {}'.format(ctx.guild.name, e))
            reply += f'\nUnknown error reloading "cogs.{cog}".  Check logs.'
        finally:
            # logger.info('Guild: {} | Reload command: {}'.format(ctx.guild.name, reply))
            await ctx.send(reply)
    # end of def reload


def setup(bot):
    global logger
    logger = logging.getLogger('discord')
    bot.add_cog(Admin(bot))
# end of def setup
