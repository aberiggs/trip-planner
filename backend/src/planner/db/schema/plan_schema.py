"""Module providing function to enforce the plan schema"""


def enforce_plan_schema(db):
    """Function that enforces plan schema in mongodb"""

    schema_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "name",
                "date",
                "owner",
            ],
            "properties": {
                "name": {
                    "bsonType": "string",
                },
                "date": {
                    "bsonType": "date",
                },
                "owner": {
                    "bsonType": "string",
                },
            },
        }
    }

    db.command("collMod", "plans", validator=schema_validator)
