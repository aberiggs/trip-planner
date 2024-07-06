"""Module that provides repository for activity"""

from planner.db.create_collection import create_collection
from planner.db.schema.activity_schema import enforce_activity_schema


class ActivityRepo:
    """Class that provides activity repository to interact with the database"""

    def __init__(self, db, session):
        self.db = db
        self.session = session
        create_collection(self.db, "activities")
        enforce_activity_schema(self.db)

    def insert_one(self, activity):
        """Function that inserts one plan"""

        return self.db.activities.insert_one(activity, session=self.session)

    def find_one_by_id(self, _id):
        """Function that finds a plan using id"""

        return self.db.activities.find_one({"_id": _id}, session=self.session)

    def update_one_by_id(self, _id, update):
        """Function that updates one plan"""

        return self.db.activities.update_one(
            {"_id": _id},
            update,
            session=self.session,
        )

    def delete_one_by_id(self, _id):
        """Function that removes one plan"""

        return self.db.activities.delete_one({"_id": _id}, session=self.session)
