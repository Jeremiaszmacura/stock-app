"""Module contains User pydantic schemas."""
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field

from schemas.py_object_id import PyObjectId


class GetStockData(BaseModel):
    symbol: str = Field(example="INTC")
    interval: str = Field(example="daily")
    calculate: list[str] = Field(example=["var", "hurst"])

    class Config:
        schema_extra = {
            "example": {
                "symbol": "INTC",
                "interval": "daily",
                "calculate": ["var", "hurst"],
            }
        }