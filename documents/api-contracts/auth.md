# Hello

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
    "email": "chiweilien3124tripplanner@gmail.com"
}
```

## Error Response

**Condition** : 

**Code** : 

**Content** :

```json
{
}
```
