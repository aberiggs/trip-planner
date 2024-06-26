"""Module providing function to enforce the activity schema"""


def enforce_activity_schema(db):
    """Function that enforce schema validation for activities collection"""

    schema_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "location", "start_time", "end_time", "note"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
                "location": {
                    "bsonType": "string",
                    "description": "must be an string and is required",
                },
                "start_time": {
                    "bsonType": "date",
                    "description": "must be a date and is required",
                },
                "end_time": {
                    "bsonType": "date",
                    "description": "must be a date and is required",
                },
                "note": {
                    "bsonType": "string",
                    "description": "must be a string and is required",
                },
            },
        }
    }

    db.command("collMod", "activities", validator=schema_validator)
