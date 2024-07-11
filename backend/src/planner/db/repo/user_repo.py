"""Module that provides repository for user"""

from planner.db.repo.repo import Repo
from planner.db.schema.user_schema import enforce_user_schema


class UserRepo(Repo):
    """Class that provides user repository to interact with the database"""

    def __init__(self, db, session):
        super().__init__(db, session, db.users, "users")
        enforce_user_schema(self.db)

    def find_one_by_email(self, email):
        """Function that finds one user by email"""

        return self.db.users.find_one({"email": email}, session=self.session)

    def update_one_by_email(self, email, update):
        """Function that updates one user"""

        return self.db.users.update_one(
            {"email": email},
            update,
            session=self.session,
        )
