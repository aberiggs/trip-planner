# Password Signup

Sign in the user with their password and email.

**URL** : `/signup`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "email": "[]",
    "password": "[]",
    "first_name": "[]",
    "last_name": "[]"
}
```

**Data example**

```json
{
    "email": "willy3124@email.com",
    "password": "this is secure",
    "first_name": "Willy",
    "last_name": "Lien"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "jwt": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOsIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjzxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJi_adQssw5c"
}
```

This JWT token can be decoded into the following fields:

```json
# header
{
  "alg": "HS256",
  "exp": "[expiration date in Unix epoch time]",
  "typ": "JWT"
}

# payload
{
    "email": "willy3124@email.com",
    "picture": "willy.png",
    "name": "Willy Lien"
}
```

## Error Response

**Condition** : Email is already used by another account

**Code** : `409 Conflict`

**Content** :

```json
{
    "message": "email already used"
}
```

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
```
