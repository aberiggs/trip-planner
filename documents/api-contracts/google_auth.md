# Google Auth

Sign in or sign up the passed in user.

**URL** : `/google_auth`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "idToken": "[idToken returned by Google Login]",
    "client_type": "web" or "ios"
}
```

**Data example**

```json
{
    "id_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
    "client_type": "web"
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

**Condition** : If the passed in `id_token` is invalid.

**Code** : `401 Unauthorized`

**Content** :

```json
{
    "message": "invalid id_token"
}
```

**Condition** : If the passed in `client_type` is invalid.

**Code** : `401 Unauthorized`

**Content** :

```json
{
    "message": "invalid client_type"
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
