"""Module contins CURD database requests for User collection."""
import pymongo
import bson
from fastapi.exceptions import HTTPException

import security as security
from database import User
from schemas.user import UserUpdate, UserCreate


async def get_users(skip: int = 0, limit: int = 100) -> list[dict]:
    users = await User.find(limit=limit, skip=skip).to_list(limit)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found.")
    for doc in users:
        doc["_id"] = str(doc["_id"])
    return users


async def get_user_by_id(user_id: str) -> dict:
    try:
        user = await User.find_one({"_id": bson.ObjectId(user_id)})
    except bson.errors.InvalidId:
        raise HTTPException(status_code=400, detail=f"Passed invalid id: {user_id}.")
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id: {user_id} not found.",
        )
    user["_id"] = str(user["_id"])
    return user


async def get_user_by_email(user_email: str) -> dict:
    user = await User.find_one({"email": user_email})
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with email: {user_email} not found.",
        )
    user["_id"] = str(user["_id"])
    return user


async def update_user(user_id: str, user: UserUpdate) -> dict:
    # remove None values from user
    user = {k: v for k, v in user.items() if v is not None}
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


async def create_user(user: UserCreate) -> dict:
    user["password"] = security.get_password_hash(user["password"])
    try:
        # returns pymongo.results.InsertOneResult (contain only _id)
        new_user = await User.insert_one(user)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=409,
            detail=f"User with such email: {user['email']} already exists.",
        )
    created_user = await User.find_one({"_id": new_user.inserted_id})

    return created_user


async def delete_user(user_id: str) -> dict:
    user = await User.find_one_and_delete({"_id": bson.ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")
    user["_id"] = str(user["_id"])
    return user
