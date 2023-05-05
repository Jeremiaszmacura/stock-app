"""Module contains User pydantic schemas."""
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field

from schemas.py_object_id import PyObjectId


class GetStockData(BaseModel):
    symbol: str = Field(example="INTC")
    interval: str = Field(example="daily")
    calculate: list[str] = Field(example=["var", "hurst"])
    var_type: str = Field(example="historical")
    confidence_level: float = Field(example=0.99)
    portfolio_value: float = Field(example=1000000)
    historical_days: int = Field(example=200)
    horizon_days: int = Field(example=10)

    class Config:
        schema_extra = {
            "example": {
                "symbol": "INTC",
                "interval": "daily",
                "calculate": ["var", "hurst"],
            }
        }