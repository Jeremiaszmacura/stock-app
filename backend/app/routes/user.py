"""Module contains endpoints for User collection."""
import json
from datetime import timedelta

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import parse_obj_as

import security as security
from config import settings
from schemas.user import UserOut, UserCreate, UserUpdate
from crud import user_crud


router = APIRouter()


@router.get("/", response_description="Users retrieved", response_model=list[UserOut])
async def get_users(skip: int = 0, limit: int = 100) -> JSONResponse:
    """Endpoint returns all users from database.

    Args:
        skip (int, optional): The number of records to skip starting from the first record \
            in the collection. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        JSONResponse: All users returned from the database
    """
    users = await user_crud.get_users(skip=skip, limit=limit)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.get("/by-email/{email}", response_description="User retrieved", response_model=UserOut)
async def get_user_by_email(email: str) -> JSONResponse:
    """Endpoint returns selected user by email from database.

    Args:
        email (str): User email.

    Returns:
        JSONResponse: User return from databse.
    """
    user = await user_crud.get_user_by_email(email)
    user = jsonable_encoder(parse_obj_as(UserOut, user))
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.get("/{user_id}", response_description="User retrieved", response_model=UserOut)
async def get_user_by_id(user_id: str) -> JSONResponse:
    """Endpoint returns selected user by id from database.

    Args:
        user_id (str): User id.

    Returns:
        JSONResponse: User return from databse.
    """
    user = await user_crud.get_user_by_id(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post("/", response_description="User created", response_model=UserOut)
async def create_students(user: UserCreate) -> JSONResponse:
    """Endpoint to create new user.

    Args:
        user (UserCreate): New user's details.

    Returns:
        JSONResponse: Newly created user.
    """
    user: dict = jsonable_encoder(user)
    if user["password"] != user["confirm_password"]:
        raise HTTPException(
            status_code=400, detail=f"Password and confirm password are not the same."
        )
    try:
        del user["confirm_password"]
    except KeyError:
        pass
    created_user = await user_crud.create_user(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.put("/{user_id}", response_description="User updated", response_model=UserOut)
async def update_user(user_id: str, user: UserUpdate) -> JSONResponse:
    """Endpoint to update seleted user's data.

    Args:
        user_id (str): User id.
        user (UserUpdate): User's details to be updated.

    Returns:
        JSONResponse: Updated user.
    """
    user = jsonable_encoder(user)
    user = await user_crud.update_user(user_id, user)
    user = jsonable_encoder(parse_obj_as(UserOut, user))
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={
            "id": user["_id"],
            "username": user["email"],
            "name": user["name"],
            "surname": user["surname"],
            "is_superuser": user["is_superuser"],
        },
        expires_delta=access_token_expires,
    )
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": user, "access_token": access_token, "token_type": "bearer"})


@router.delete("/{user_id}", response_description="User deleted", response_model=UserOut)
async def delete_user(user_id: str) -> JSONResponse:
    """Endpoint to delete selected user.

    Args:
        user_id (str): User id.

    Returns:
        JSONResponse: Deleted user.
    """
    user = await user_crud.delete_user(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)
