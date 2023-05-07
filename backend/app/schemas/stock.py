"""Module contains User pydantic schemas."""
from datetime import datetime
from bson.objectid import ObjectId
from pydantic import BaseModel, EmailStr, Field

from schemas.py_object_id import PyObjectId


class GetStockData(BaseModel):
    symbol: str = Field(example="INTC")
    name: str = Field(example="Intel Corp")
    type: str = Field(example="Equity")
    region: str = Field(example="United States")
    market_open: str = Field(example="09:30")
    market_close: str = Field(example="16:00")
    timezone: str = Field(example="UTC-04")
    currency: str = Field(example="USD")
    calculate: list[str] = Field(example=["var", ""])
    interval: str | None = Field(example="daily")
    var_type: str | None = Field(example="historical")
    portfolio_value: float | None = Field(example=1000)
    confidence_level: float | None = Field(example=0.99)
    historical_days: int | None = Field(example=200)
    horizon_days: int | None = Field(example=1)
    plot: str | None
    var: float | None

    class Config:
        orm_mode = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "symbol": "INTC",
                "name": "Intel Corp",
                "type": "Equity",
                "region": "United States",
                "market_open": "09:30",
                "market_close": "16:00",
                "timezone": "UTC-04",
                "currency": "USD",
                "calculate": ["var", ""],
                "interval": "daily",
                "var_type": "historical",
                "portfolio_value": 1000,
                "confidence_level": 0.99,
                "historical_days": 200,
                "horizon_days": 1,
            }
        }
