# Test Auth

Test whether the user is signed in. This API is for development use only and will be removed on final production.

**URL** : `/test_auth`

**Method** : `GET`

**Auth required** : NO

**Data constraints**

Header:
```json
{
    "Authorization": "Bearer [Bearer token]"
}
```

**Data example**

```json
{
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOsIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjzxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJi_adQssw5c"
}
```

## Success Response

**Code** : `200 OK`

**Content example**

```json
{
    "message": "you are logged in"
}
```

## Error Response

**Condition** : If the passed in `Bearer token` is invalid.

**Code** : `401 Unauthorized`

**Content** :

```json
{
    "message": "you are not logged in"
}
```
