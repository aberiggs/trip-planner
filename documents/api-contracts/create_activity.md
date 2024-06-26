# Create Activity

Create an activity document in activities collection.

**URL** : `/create_activity`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "name": "[]",
    "location": "[]",
    "start_time": "[%m/%d/%y %H:%M:%S]",
    "end_time": "[%m/%d/%y %H:%M:%S]",
    "note": "[]"
}
```

**Data example**

```json
{
    "name": "Party",
    "location": "NYC",
    "start_time": "09/19/22 13:55:26",
    "end_time": "09/19/22 15:35:12",
    "note": "bring some drinks"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "inserted_id": "667b6c2e208a004c179d689a"
}
```


## Error Response

**Condition** : If the passed in request body is an invalid JSON.

**Code** : `400 Bad Request`

**Content** :

```json
{
    "message": "request body is an invalid JSON"
}
```

**Condition** : If the required fields are missing in body

**Code** : `400 Bad Request`

**Content** :

```json
{
    "message": "The following fields are missing in body: [missing fields]"
}
