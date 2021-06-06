import sys
import logging
import logging.handlers
# import os
# import asyncio
# import glob
# import traceback
import discord


def logsetup():
    #
    # CONFIGURE LOGS
    #
    # logging level can be CRITICAL, ERROR, WARNING, INFO, and DEBUG
    # and if not specified defaults to WARNING
    
    # what modules create logs?
    # print("Modules with loggers:")
    # for key in logging.Logger.manager.loggerDict.keys():
    #     print(key)
    # end of for key
    # print("-------------")
    
    LOG_OBJ_NAME = __file__[0:-3] + "_logger"
    LOG_FILE = __file__[0:-3] + ".log"
    LOG_FORMAT = '%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s'
    FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s')
    
    # set the basicConfig
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s')
    
    logger = logging.getLogger(LOG_OBJ_NAME)
    logger.info('Main: Logs started.')
    print("bot logs will be collected in the log file ({})".format(LOG_FILE))
    
    # silence info logs from discord library
    # dlogs = logging.getLogger("discord.gateway")
    # dlogs.setLevel(logging.WARNING)
    # dlogs.propagate = False
    
    
    #
    # move discord library logs to the console
    #
    # create the handler
    dloghandler = logging.StreamHandler(sys.stdout)
    # create the formatter
    dlogformat = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s')
    # add the formatter to the handler
    dloghandler.setFormatter(dlogformat)
    
    dlogs1 = logging.getLogger("discord.gateway")
    # add the handler to the logger
    dlogs1.addHandler(dloghandler)
    # set the logging level
    dlogs1.setLevel(logging.INFO)
    # stop the logs from propagating up
    dlogs1.propagate = False
    
    dlogs2 = logging.getLogger("discord.state")
    # add the handler to the logger
    dlogs2.addHandler(dloghandler)
    # set the logging level
    dlogs2.setLevel(logging.INFO)
    # stop the logs from propagating up
    dlogs2.propagate = False
    
    # move the client to stdout because we get _connect/resume every few hours
    dlogs3 = logging.getLogger("discord.client")
    # add the handler to the logger
    dlogs3.addHandler(dloghandler)
    # set the logging level
    dlogs3.setLevel(logging.INFO)
    # stop the logs from propagating up
    dlogs3.propagate = False
    
    print('discord.py library logs will be shown here (stdout).')
    
#
# logme function to simplify logging with context info
#
def logme(level, ctx, logstr):
    # Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').

    if ctx.author.nick == None:
        nick = ctx.author.name
    else:
        nick = ctx.author.nick
        
    if (level == "info"):
        logger.info(f'[{ctx.guild.name} | {ctx.channel.name}] {nick}/{ctx.author.name}: {logstr}')
    elif level == "warning":
        logger.warning(f'[{ctx.guild.name} | {ctx.channel.name}] {nick}/{ctx.author.name}: {logstr}')
    elif level == "exception":
        logger.exeption(f'[{ctx.guild.name} | {ctx.channel.name}] {nick}/{ctx.author.name}: {logstr}')
    elif level == "error":
        logger.error(f'[{ctx.guild.name} | {ctx.channel.name}] {nick}/{ctx.author.name}: {logstr}')
    elif level == "critical":
        logger.critical(f'[{ctx.guild.name} | {ctx.channel.name}] {nick}/{ctx.author.name}: {logstr}')
    else:
        logger.info(f'[{ctx.guild.name} | {ctx.channel.name}] {nick}/{ctx.author.name}: {logstr}')


