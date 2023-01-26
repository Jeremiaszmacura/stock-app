def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "surname": user["surname"],
        "is_active": user["is_active"],
        "is_superuser": user["is_superuser"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def userResponseEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"],
        "is_active": user["is_active"],
        "is_superuser": user["is_superuser"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def embeddedUserResponse(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "name": user["name"]
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]

