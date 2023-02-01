import pymongo
from bson.objectid import ObjectId
from fastapi.exceptions import HTTPException

from database import User
from schemas.user import UserUpdate


async def get_users(skip: int = 0, limit: int = 100) -> list[dict]:
    users = await User.find(limit=limit, skip=skip).to_list(limit)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found.")
    for doc in users:
        doc["_id"] = str(doc["_id"])
    return users


async def get_user(user_id: str) -> dict:
    user = await User.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")
    user["_id"] = str(user["_id"])
    return user


async def update_user(user_id: str, user: UserUpdate) -> dict:
    user_id = ObjectId(user_id)
    if len(user) >= 1:
        update_result = await User.update_one({"_id": user_id}, {"$set": user})
        if update_result.modified_count == 1:
            user = await User.find_one({"_id": user_id})
            if (updated_student := await User.find_one({"_id": user_id})) is not None:
                updated_student["_id"] = str(updated_student["_id"])
                return updated_student
    if (existing_student := await User.find_one({"_id": user_id})) is not None:
        existing_student["_id"] = str(existing_student["_id"])
        return existing_student
    raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")


async def create_user(user: dict) -> dict:
    try:
        new_user = await User.insert_one(
            user
        )  # returns pymongo.results.InsertOneResult (contain only _id)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"User with such email: {user['email']} already exists.",
        )
    user = await User.find_one({"_id": new_user.inserted_id})

    return user


async def delete_user(user_id: str) -> dict:
    user = await User.find_one_and_delete({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")
    user["_id"] = str(user["_id"])
    return user
