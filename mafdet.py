import sys
import logging
import logging.handlers
# import os
# import asyncio
# import glob
# import traceback
import discord

from discord.ext import commands
from config.settings import SETTINGS

# add threaded web server so repl.it will stay active
# with help from uptimerobot
from flask import Flask
from flask import send_file

import threading
import os
import time

# from multiprocessing import Process


print('Starting up.')


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

#
# Setup the bot
#
logger.info('Main: Starting bot')

# pollmaster has its own help, so don't know if pm_help : False
# should be included in bot_config or not
#    'pm_help' : False,

# Discord intents and privledged intents require setting on both the bot web page and in code
# don't know if default is too restrictive and don't have time to research, so use all for now
# intents = discord.Intents.default()

# Update March 2021: due to error on my part, ran old version of Mafdet and found that 
# intents.members is needed to get the member_listener cog to run properly, so just use that for now.
# intents = discord.Intents.all()
intents = discord.Intents.default()
intents.members = True

bot_config = {
    'command_prefix'        : '.',
    'commands_on_edit'      : True,
    'status'                : discord.Status.online,
    'owner_id'              : int(os.environ['owner_id']),
    'fetch_offline_members' : False,
    'max_messages'          : 15000,
    'case_insensitive'      : True,
    'heartbeat_timeout'     : 240,
    'description'           : 'Mafdet v3.1',
    'intents'               : intents
}

bot = commands.Bot(**bot_config)

# remove the built-in help command.  It will be added via separate cog
# bot.remove_command('help')
# while creating the help cog, use .helpme instead

#
# Make a list of aliases for Mafdet to choose from in embed messages
#
# duplicate some author names to bias the randomness
bot.mafdetlist = ["Mafdet, goddess of judgement, justice, and execution says",
              "Mafdet, Slayer of Serpents says",
              "Mafdet, The Great Cat says",
              "Mafdet, goddess of judgement, justice, and execution says",
              "Mafdet, Slayer of Serpents says"]


#
# Extensions
#

coglist = []
try:
    with open('config/approved_cogs.txt', 'r') as f:
        for line in f:
            coglist.append(line.strip())
        logger.info('Main: coglist: {}'.format(coglist))
except Exception as err:
    logger.warning('Main: Error reading cog list!')
    logger.warning(err)
    exit()

for cog in coglist:
    cogfile = 'cogs.' + cog[:-3]
    try:
        bot.load_extension(cogfile)
    except Exception as err:
        print('{}'.format(err))
        #traceback.print_exc(err)
logger.info('Main: Extensions loaded')

''' # for debugging
for x in bot.cogs:
    logger.info('Main: {}'.format(x))

for x in bot.commands:
    logger.info('Main: {}'.format(x))
'''

''' # comment out before_invoke and after_invoke until needed
@bot.before_invoke
async def before_any_command(ctx):
    # do something before a command is called
    logger.info('Main: Executing bot.before_invoke')
    pass
# end of before_invoke

@bot.after_invoke
async def after_any_command(ctx):
    # do something after a command is called
    logger.info('Main: Executing bot.after_invoke')
    pass
# end of after_invoke
'''


#
# Events
#
@bot.event
async def on_ready():
    logger.info("Main: Bot logged in and ready!")
    logger.info("Main: username: " + bot.user.name)
    logger.info("Main: id: " + str(bot.user.id))
    logger.info("Main: owner: " + str(bot.owner_id))
    # for guild in bot.guilds:
    #    if guild.system_channel:
    #        await guild.system_channel.send("Mafdet is online!")
    # end of for guild

    # set presence
    try:
        myname = 'for {}help'.format(bot.command_prefix)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=myname))
        logger.info('Main: Setting presence')
    except Exception as error:
        logger.warning('Main: Error setting presence: {}'.format(error))
    # end of try set presence
# end of on_ready

@bot.event
async def on_shard_ready():
    logger.info("Main: on_shard_ready event fired")
    for guild in bot.guilds:
        logger.info("Main: Guild and shard_id: " + guild.name + " | " + guild.shard_id)
    # end of for guild
# end of on_shard_ready

'''
# take out the on_resumed event.  It's generated a lot from discord disconnecting and reconnecting
# every few hours.  Need to block the _connect log message from the discord client.py package, too (see above)
#async def on_resumed():
    logger.info("Main: connection resumed")
# end of on_resumed
'''

#
# Built-in Commands
#
@bot.command()
async def ping(ctx):
    '''Simple latency test'''
    latency = bot.latency
    await ctx.send("Pong: {}".format(latency))
    logme("info", ctx, "inside ping")

# per-command before_ and after_ invokes, too!
'''
@ping.before_invoke
async def before_ping_command(ctx):
    # do something before the ping command is called
    logger.info('Main: Executing ping.before_invoke')
    pass

@ping.after_invoke
async def after_ping_command(ctx):
    # do something after the ping command is called
    logger.info('Main: Executing ping.after_invoke')
    pass
'''
# end of ping command

#
# start up keep alive Flask server
#
logger.info('create app')
app = Flask('mafdet_keep_alive_server')

@app.route("/")
def hello_world():
    logger.info('inside hello_world')
    return "<p>Hello, World!</p>"

@app.route("/test", methods=['GET'])
def test():
    logger.info('inside flask test')
    return send_file(
            'hb30.4.2.jpg',
            as_attachment=False,
            attachment_filename='hb30.4.2.jpg',
            mimetype='image/jpeg'
    )

def run():
  app.run(host='0.0.0.0',port=8000)

def keep_alive():  
    t = threading.Thread(target=run)
    t.start()

logger.info('start keep alive server')
keep_alive()
logger.info('keep aliv server started')

#
# Turn on the bot!
#
bot_token = os.environ['my_token']
bot.run(bot_token)

logger.info('Main: after bot.run')

exit()