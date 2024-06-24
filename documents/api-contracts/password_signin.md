# Google Auth

Sign in the user with their password and email.

**URL** : `/signin`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "email": "[user email]",
    "password": "[user password]"
}
```

**Data example**

```json
{
    "email": "willy3124@email.com",
    "password": "this is secure"
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
    "email": "[user's email]",
    "picture": "[user's profile picture]",
    "name": "[user's first and last name]"
}
```

## Error Response

**Condition** : User doesn't exist

**Code** : `401 Unauthorized`

**Content** :

```json
{
    "message": "user doesn't exist or password incorrect"
}
```

**Condition** : Password incorrect

**Code** : `401 Unauthorized`

**Content** :

```json
{
    "message": "user doesn't exist or password incorrect"
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
