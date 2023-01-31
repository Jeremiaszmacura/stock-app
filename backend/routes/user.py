from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from schemas.user import UserOut, UserCreate
from crud import user_crud


router = APIRouter()


@router.get("/", response_description="Users retrieved", response_model=list[UserOut])
async def get_users(skip: int = 0, limit: int = 100) -> dict:
    users = await user_crud.get_users(skip=skip, limit=limit)
    return JSONResponse(status_code=status.HTTP_200_OK, content=users)


@router.get("/{user_id}", response_description="User retrieved", response_model=UserOut)
async def get_user(user_id: str) -> dict:
    user = await user_crud.get_user(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)


@router.post("/", response_description="User created", response_model=UserOut)
async def create_students(user: UserCreate) -> JSONResponse:
    user = jsonable_encoder(user)
    created_user = await user_crud.create_user(user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user)


@router.delete("/{user_id}", response_description="User deleted")
async def delete_user(user_id: str) -> dict:
    user = await user_crud.delete_user(user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content=user)
