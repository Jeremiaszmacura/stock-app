from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field

from schemas.py_object_id import PyObjectId


class UserBase(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr | None = Field(example="email@email.com")
    name: str = Field(title="User Name", max_length=30, example="John")
    surname: str = Field(title="User Name", max_length=30, example="Kowalsky")
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "email": "email@email.com",
                "name": "John",
                "surname": "Kowalsky",
                "is_active": True,
                "is_superuser": False,
            }
        }


class UserCreate(UserBase):
    password: str = Field(title="User password", max_length=40)
    confirm_password: str = Field(title="Confirm user password", max_length=40)

    class Config:
        schema_extra = {
            "example": {
                "name": "John",
                "surname": "Kowalsky",
                "email": "email@email.com",
                "is_active": True,
                "is_superuser": False,
                "password": "Chdo123mFdu@S54",
                "confirm_password": "Chdo123mFdu@S54",
            }
        }


class UserInDB(UserBase):
    hashed_password: str


class UserOut(UserBase):
    pass
