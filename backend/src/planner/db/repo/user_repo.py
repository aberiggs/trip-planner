"""Module that provides repository for user"""

from planner.db.repo.repo import Repo

class UserRepo(Repo):
    """Class that provides user repository to interact with the database"""

    def __init__(self, db, session):
        super().__init__(db, session, "users")

    def find_one_by_email(self, email):
        """Function that finds one user by email"""

        return self.collection.find_one({"email": email}, session=self.session)

    def update_one_by_email(self, email, update):
        """Function that updates one user"""

        return self.collection.update_one(
            {"email": email},
            update,
            session=self.session,
        )
