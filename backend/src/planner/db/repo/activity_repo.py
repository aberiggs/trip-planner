"""Module that provides repository for activity"""

from planner.db.repo.repo import Repo

class ActivityRepo(Repo):
    """Class that provides activity repository to interact with the database"""

    def __init__(self, db, session):
        super().__init__(db, session, "activities")
