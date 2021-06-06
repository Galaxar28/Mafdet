class Secrets:
    def __init__(self):

        # Oops - don't put the bot token in GitHub!  Discord found it when uploaded and reset the token.
        self.bot_token = 'bot_token_goes_here' # mafdet token

        # self.mode = 'development' # or production

SECRETS = Secrets()
