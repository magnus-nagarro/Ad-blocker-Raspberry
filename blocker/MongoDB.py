from __init__ import *


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
            return {"success": False,
                    "error": "URL exists already"}
        try:
            collection.insert_one(insert_buffer)
            return {"success": True}
        except Exception as e:
            return {"success": False,
                    "error": e}

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

    def delete_links(self, link):
        database = self.client["Links"]
        collection = database["Blocked"]
        exists = collection.find_one({"link": link})
        if exists:
            try:
                collection.delete_one({"link": link})
                return {"success": True}
            except Exception as e:
                return {"success": False,
                        "error": e}
        return {"success": False,
                "error": "Link not found in the Database!"}