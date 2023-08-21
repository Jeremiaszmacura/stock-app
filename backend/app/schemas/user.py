"""Module contains User pydantic schemas."""
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field

from schemas.py_object_id import PyObjectId
from schemas.stock import GetStockData


class UserBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr = Field(example="email@email.com")
    name: str = Field(title="User Name", max_length=30, example="John")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    analysis_history: list[GetStockData] = Field(default=[])

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "name": "John",
                "is_active": True,
                "is_superuser": False,
            }
        }


class UserCreate(UserBase):
    password: str = Field(title="User password", max_length=40)
    confirm_password: str = Field(title="Confirm user password", max_length=40)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "email": "email@email.com",
                "is_active": True,
                "is_superuser": False,
                "password": "Chdo123mFdu@S54",
                "confirm_password": "Chdo123mFdu@S54",
            }
        }


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(example="email@email.com")
    name: str | None = Field(title="User Name", max_length=30, example="John")
    is_active: bool | None = Field(default=True)
    is_superuser: bool | None = Field(default=False)
    updated_at: datetime | None = Field(default=datetime.now())
    password: str | None = Field(title="User password", max_length=40)
    confirm_password: str | None = Field(title="Confirm user password", max_length=40)
    analysis_history: list[GetStockData] | None = Field(default=[])

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "name": "John",
                "is_active": True,
                "is_superuser": False,
            }
        }


class UserInDB(UserBase):
    hashed_password: str


class UserOut(UserBase):
    pass
