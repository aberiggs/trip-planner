"""Module providing function to enforce the user schema"""


def enforce_user_schema(db):
    """Function that enforces user schema in mongodb"""

    schema_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "first_name",
                "last_name",
                "last_visited",
                "email",
                "google_login",
            ],
            "properties": {
                "first_name": {
                    "bsonType": "string",
                },
                "last_name": {
                    "bsonType": "string",
                },
                "last_visited": {
                    "bsonType": "date",
                },
                "picture": {
                    "bsonType": "string",
                },
                "email": {
                    "bsonType": "string",
                },
                "password": {
                    "bsonType": "binData",
                },
                "google_login": {
                    "bsonType": "bool",
                },
                "plans": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId",
                    },
                },
            },
        }
    }

    db.command("collMod", "users", validator=schema_validator)
