"""Endpoints for User collection."""
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

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


@router.get("/{user_id}", response_description="User retrieved", response_model=UserOut)
async def get_user(user_id: str) -> JSONResponse:
    """Endpoint returns selected user by id from database.

    Args:
        user_id (str): User id.

    Returns:
        JSONResponse: User return from databse.
    """
    user = await user_crud.get_user(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post("/", response_description="User created", response_model=UserOut)
async def create_students(user: UserCreate) -> JSONResponse:
    """Endpoint to create new user.

    Args:
        user (UserCreate): New user's details.

    Returns:
        JSONResponse: Newly created user.
    """
    user = jsonable_encoder(user)
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
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


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
