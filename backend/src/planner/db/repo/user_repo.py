"""Module that provides repository for user"""

from planner.db.create_collection import create_collection
from planner.db.schema.user_schema import enforce_user_schema


class UserRepo:
    """Class that provides user repository to interact with the database"""

    def __init__(self, db, session):
        self.db = db
        self.session = session
        create_collection(self.db, "users")
        enforce_user_schema(self.db)

    def find_one_by_email(self, email):
        """Function that finds one user by email"""

        return self.db.users.find_one({"email": email}, session=self.session)

    def insert_one(self, user):
        """Function that inserts one user"""

        return self.db.users.insert_one(user, session=self.session)

    def update_one(self, email, update):
        """Function that updates one user"""

        return self.db.users.update_one(
            {"email": email},
            update,
            session=self.session,
        )
