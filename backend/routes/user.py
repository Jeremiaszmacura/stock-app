from fastapi import APIRouter, Body

from schemas.user import UserOut
from crud import user_crud


router = APIRouter()


@router.get("/", response_description="Users retrieved")
def get_users(skip: int = 0, limit: int = 100) -> dict:
    users = user_crud.get_users(skip=skip, limit=limit)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Users data retrieved successfully",
        "data": users
    }


@router.post("/", response_description="User created")
def create_students() -> dict:
    result_id = user_crud.create_users()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "New user created successfully",
        "data": result_id
    }
