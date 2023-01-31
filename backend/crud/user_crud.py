import pymongo
from bson.objectid import ObjectId
from fastapi.exceptions import HTTPException

from database import User


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


async def create_user(user: dict) -> dict:
    try:
        new_user = await User.insert_one(user) # returns pymongo.results.InsertOneResult (contain only _id)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=409, detail=f"User with such email: {user['email']} already exists.")
    user = await User.find_one({"_id": new_user.inserted_id})
    
    return user


async def delete_user(user_id: str) -> dict:
    user = await User.find_one_and_delete({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")
    user["_id"] = str(user["_id"])
    return user