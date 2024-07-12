"""Module that provides repository for plan"""

from planner.db.repo.repo import Repo

class PlanRepo(Repo):
    """Class that provides plan repository to interact with the database"""

    def __init__(self, db, session):
        super().__init__(db, session, "plans")
