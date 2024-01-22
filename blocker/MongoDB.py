from pymongo import MongoClient


class mongodb:
    def __init__(self) -> None:
        self.client = self.get_database()

    def get_database(self):
        CONNECTION_STRING = "mongodb://mongodb:27017"
        client = MongoClient(CONNECTION_STRING)
        return client

    def add_links(self, link):
        database = self.client["Links"]
        collection = database["Blocked"]
        insert_buffer = {
            "link": link,
        }
        exists = collection.find_one(insert_buffer)
        if exists:
            return f"{False}, Link exists already!"
        try:
            collection.insert_one(insert_buffer)
            return True
        except Exception as e:
            return f"{False}, Error: {e}"
