from pymongo import MongoClient



class Mongo(MongoClient):
    def __init__(self, bot, **kwargs):
        super().__init__(host=bot.config["mongo"], **kwargs)
        self._db = self.livecord # Database object

        self.notifications = self._db.notifs