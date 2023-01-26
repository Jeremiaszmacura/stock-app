from serializers.user_serializers import userResponseEntity
from database import User
from schemas.user import UserOut


def get_users(skip: int = 0, limit: int = 100) -> list[dict]:
    users = list(User.find(limit=limit, skip=skip))
    for doc in users:
        doc["_id"] = str(doc["_id"])
    return users


def create_users() -> str:
    user = {
                "name": "John",
                "surname": "Kowalsky",
                "email": "email1@email.com",
                "is_active": True,
                "is_superuser": False,
                "password": "Chdo123mFdu@S54",
            }
    response = User.insert_one(user) # returns pymongo.results.InsertOneResult (contain only _id)
    response = str(response.inserted_id)
    return response