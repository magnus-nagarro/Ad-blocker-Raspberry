from __init__ import MongoClient


class mongodb:
    def __init__(self) -> None:
        self.client = self.get_database()

    # Creating a MongoClient and returning it, is beeing called in init to create a member variable of Type MongoClient -> MongoClient
    def get_database(self):
        CONNECTION_STRING = "mongodb://localhost:27017"
        client = MongoClient(CONNECTION_STRING)
        return client

    # Checks if the blocker should currently run -> bool
    def should_blocker_run(self):
        database = self.client["Running"]
        try:
            # Returns all collection names inside the "Running" database
            names = database.list_collection_names()
        except Exception as e:
            print(e)
            return False
        for name in names:
            buff = name.find('dummy')
            # If the list of collection names contains dummy that means the blocker should run so we return true
            if buff != -1:
                return True
            else:
                continue
        return False

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
                print(e)
                return False
        return return_buffer
