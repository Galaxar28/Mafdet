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

        self.bot_token = 'NjE3NDAwMjIwMjk2NDEzMTk2.XWqoCA.jT_K8Z3fUumxaEVnGSQEcDog8hw' # mafdet token

        # self.mode = 'development' # or production

SECRETS = Secrets()
