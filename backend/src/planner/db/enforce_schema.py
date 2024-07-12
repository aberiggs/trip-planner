"""Module providing function to enforce schema"""

schema_validators = {
    "activities" : {
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
    },
    "plans" : {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "name",
                "date",
                "owner",
                "members",
                "activities"
            ],
            "properties": {
                "name": {
                    "bsonType": "string",
                },
                "date": {
                    "bsonType": "date",
                },
                "owner": {
                    "bsonType": "objectId",
                },
                "members": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId",
                    },
                },
                "activities": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "objectId",
                    },
                },
            },
        }
    },
    "users" : {
        "$jsonSchema": {
            "bsonType": "object",
            "required": [
                "first_name",
                "last_name",
                "last_visited",
                "email",
                "google_signup",
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
                "google_signup": {
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

}

def enforce_schema(db, collection_name):
    """Function that enforce schema validation for {collection_name} collection"""
    db.command("collMod", "activities", validator=schema_validators[collection_name])
