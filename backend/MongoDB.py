from __init__ import MongoClient


class mongodb:
    def __init__(self) -> None:
        self.client = self.get_database()

    # Creating a MongoClient and returning it, is beeing called in init to create a member variable of Type MongoClient -> MongoClient
    def get_database(self):
        CONNECTION_STRING = "mongodb://mongodb:27017"
        client = MongoClient(CONNECTION_STRING)
        return client

    # Adding links to the database, while checking that the link does not exist yet -> bool
    def add_links(self, link):
        database = self.client["Links"]
        collection = database["Blocked"]
        # We make a dict because dicts are super easy to work with when using MongoDB
        insert_buffer = {
            "link": link,
        }
        # Does link exist already? If yes we return an error message
        exists = collection.find_one(insert_buffer)
        if exists:
            return {"success": False,
                    "error": "URL exists already"}
        # If the link does not exist we insert it into the database
        try:
            collection.insert_one(insert_buffer)
            return {"success": True}
        # Return a error message if inserting the link failed for any reason
        except Exception as e:
            return {"success": False,
                    "error": e}

    # Returns all links that should be blocked -> bool(if unsuccessful)/list
    def return_links(self):
        database = self.client["Links"]
        collection = database["Blocked"]
        # We save every document of the "Blocked" collection in "links"
        links = collection.find({})
        return_buffer = list()
        # We need to iterate through "links", since that is a list of objects and we are only interested in the "link" field
        for link in links:
            try:
                return_buffer.append(link["link"])
            except Exception as e:
                return {"success": False,
                        "error": e}
        return return_buffer

    # Deletes a link from the datbase -> bool
    def delete_links(self, link):
        database = self.client["Links"]
        collection = database["Blocked"]
        # Does the link exist?
        exists = collection.find_one({"link": link})
        if exists:
            # Delete the link
            try:
                collection.delete_one({"link": link})
                return {"success": True}
            except Exception as e:
                return {"success": False,
                        "error": e}
        return {"success": False,
                "error": "Link not found in the Database!"}

    # This function creates a new document and collection if the blocker should run, we can later check from the Blocker if that
    # collection exists and operate depending on that -> bool(if unsuccessful)/void
    def blocker_on_off(self, running):
        database = self.client["Running"]
        collection = database["dummy"]
        # if running is True we add dummy
        if running:
            dummy_data = {
                "dummy": 1
            }
            try:
                collection.insert_one(dummy_data)
            except Exception as e:
                return {"success": False,
                        "error": e}
        # if running is false we drop the dummy collection
        else:
            collection.drop()
