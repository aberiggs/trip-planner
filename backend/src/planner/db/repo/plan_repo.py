"""Module that provides repository for plan"""

from planner.db.repo.repo import Repo
from planner.db.schema.plan_schema import enforce_plan_schema


class PlanRepo(Repo):
    """Class that provides plan repository to interact with the database"""

    def __init__(self, db, session):
        super().__init__(db, session, db.plans, "plans")
        enforce_plan_schema(self.db)
