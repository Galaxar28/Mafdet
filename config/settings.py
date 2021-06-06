import discord

from config.secrets import SECRETS

class Settings:
    def __init__(self):
        self.color = discord.Colour(int('660000', 16)) # dark red, triad is 003C0D (green) and 00327A (blue)

        # this is the pollmaster icon          self.title_icon = "https://i.imgur.com/vtLsAl8.jpg" #PM
        # this is the pollmaster tag icon      self.author_icon = "https://i.imgur.com/TYbBtwB.jpg" #tag
        # this is the pollmaster report icon   self.report_icon = "https://i.imgur.com/YksGRLN.png" #report
        
        self.owner_id = 435170406748520448 # Galaxar
        self.msg_errors = False
        self.log_errors = True

        # do this later 
        # self.invite_link = \
#             'https://discordapp.com/api/oauth2/authorize?client_id=444831720659877889&permissions=126016&scope=bot'

        self.load_secrets()

    def load_secrets(self):
        # secret
        # from pollmaster  self.dbl_token = SECRETS.dbl_token
        # from pollmaster  self.mongo_db = SECRETS.mongo_db

        self.bot_token = SECRETS.bot_token

        # self.mode = SECRETS.mode

SETTINGS = Settings()
