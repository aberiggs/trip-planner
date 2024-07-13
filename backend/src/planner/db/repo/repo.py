"""Module that provides repository class"""

from planner.db.create_collection import create_collection
from planner.db.enforce_schema import enforce_schema

class Repo:
    """Parent class that provides repository to interact with the database"""

    def __init__(self, db, session, collection_name):
        self.db = db
        self.session = session
        self.collection = db[collection_name]
        self.collection_name = collection_name
        create_collection(db, collection_name)
        enforce_schema(db, collection_name)

    def insert_one(self, document):
        """Function that inserts one document"""

        return self.collection.insert_one(document, session=self.session)

    def find_one_by_id(self, _id):
        """Function that finds a document using id"""

        return self.collection.find_one({"_id": _id}, session=self.session)

    def update_one_by_id(self, _id, update):
        """Function that updates one document"""

        return self.collection.update_one(
            {"_id": _id},
            update,
            session=self.session,
        )

    def delete_one_by_id(self, _id):
        """Function that removes one document"""

        return self.collection.delete_one({"_id": _id}, session=self.session)
