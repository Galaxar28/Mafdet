class Secrets:
    def __init__(self):
        # from pollmaster  self.dbl_token = ''  # DBL token (only needed for public bot)

        # try to use mongo db in the cloud
        # copied these lines from mongo webpage
        # client = pymongo.MongoClient("mongodb+srv://<username>:<password>@mpl-mongo-cluster-y8c6g.mongodb.net/test?retryWrites=true&w=majority")
        # db = client.test
        #
        # use this instead 
        # self.mongo_db = "mongodb+srv://pollmaster_mongodb:Pufcib-ricben-boxpe6@mpl-mongo-cluster-y8c6g.mongodb.net/test?retryWrites=true&w=majority"

        # lines form original pollmaster
        # self.mongo_db = 'mongodb://localhost:27017/pollmaster'

        # Oops - don't put the bot token in GitHub!  Discord found it when uploaded and reset the token.
        self.bot_token = 'bot_token_goes_here' # mafdet token

        # self.mode = 'development' # or production

SECRETS = Secrets()
