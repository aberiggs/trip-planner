"""Module providing function to enforce the activity schema"""


def enforce_activity_schema(db):
    """Function that enforce schema validation for activities collection"""

    schema_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "name",
                "plan_id",
                "location",
                "start_time",
                "end_time",
                "note"
            ],
            "properties": {
                "name": {
                    "bsonType": "string",
                },
                "plan_id": {
                    "bsonType": "objectId",
                },
                "location": {
                    "bsonType": "string",
                },
                "start_time": {
                    "bsonType": "date",
                },
                "end_time": {
                    "bsonType": "date",
                },
                "note": {
                    "bsonType": "string",
                },
            },
        }
    }

    db.command("collMod", "activities", validator=schema_validator)
