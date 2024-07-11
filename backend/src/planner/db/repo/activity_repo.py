"""Module that provides repository for activity"""

from planner.db.repo.repo import Repo
from planner.db.schema.activity_schema import enforce_activity_schema


class ActivityRepo(Repo):
    """Class that provides activity repository to interact with the database"""

    def __init__(self, db, session):
        super().__init__(db, session, db.activities, "activities")
        enforce_activity_schema(self.db)
