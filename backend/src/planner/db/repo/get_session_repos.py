"""Module providing function to retrieve all repositories"""


from planner.db.db_init import db_init
from planner.db.repo.user_repo import UserRepo
from planner.db.repo.plan_repo import PlanRepo
from planner.db.repo.activity_repo import ActivityRepo

def get_session_repos():
    """Function that provides all repositories as a dictionary"""

    client, session = db_init()
    db = client.trip_planner
    user_repo = UserRepo(db, session)
    plan_repo = PlanRepo(db, session)
    activity_repo = ActivityRepo(db, session)
    return {
        "user": user_repo,
        "plan": plan_repo,
        "activity": activity_repo
    }
