"""Module that provides repository for plan"""

from planner.db.create_collection import create_collection
from planner.db.schema.plan_schema import enforce_plan_schema


class PlanRepo:
    """Class that provides plan repository to interact with the database"""

    def __init__(self, db, session):
        self.db = db
        self.session = session
        create_collection(self.db, "plans")
        enforce_plan_schema(self.db)

    def insert_one(self, plan):
        """Function that inserts one plan"""

        return self.db.plans.insert_one(plan, session=self.session)
