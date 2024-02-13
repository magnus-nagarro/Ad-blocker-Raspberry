from __init__ import *


class mongodb:
    def __init__(self) -> None:
        self.client = self.get_database()

    def get_database(self):
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = MongoClient(CONNECTION_STRING)
        return client

    def should_blocker_run(self):
        database = self.client["Running"]
        names = database.list_collection_names()
        for name in names:
            buff = name.find('dummy')
            if buff != -1:
                return True
            else:
                continue
        return False

    def logger(self, ip):
        database = self.client["Logged"]
        collection = database["Packets"]

        data = {
            "packet": ip,
        }

        try:
            collection.insert_one(data)
            return True
        except:
            return False

    def return_links(self):
        database = self.client["Links"]
        collection = database["Blocked"]
        links = collection.find({})
        return_buffer = list()
        for link in links:
            try:
                return_buffer.append(link["link"])
            except Exception as e:
                return {"success": False,
                        "error": e}
        return return_buffer
