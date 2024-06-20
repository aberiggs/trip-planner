def enforce_activities_schema_validation(db):
    activities_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "location", "start_time", "end_time", "note"],
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "location": {
                    "bsonType": "string",
                    "description": "must be an string and is required",
                },
                "start_time": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "end_time": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "note": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                }
            }
        }
    }

    db.command("collMod", "activities", validator=activities_validator)
    