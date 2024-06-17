# Auth

Sign in or sign up the passed in user.

**URL** : `/auth`

**Method** : `POST`

**Auth required** : NO

**Data constraints**

```json
{
    "idToken": "[idToken returned by Google Login]"
}
```

**Data example**

```json
{
    "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
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

**Condition** : If the passed in `idToken` is invalid.

**Code** : `401 Unauthorized`

**Content** :

```json
{
    "message": "invalid token"
}
```
