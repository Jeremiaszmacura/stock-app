# """Module contains endpoints for User collection."""
# from fastapi import APIRouter, status
# from fastapi.responses import JSONResponse
# from fastapi.encoders import jsonable_encoder
# from fastapi.exceptions import HTTPException
# import pandas as pd
# import matplotlib.pyplot as plt
# from alpha_vantage.timeseries import TimeSeries

# from schemas.user import UserOut, UserCreate, UserUpdate


# router = APIRouter()


# @router.get("/", response_description="Users retrieved", response_model=list[UserOut])
# async def get_users(skip: int = 0, limit: int = 100) -> JSONResponse:

#     return JSONResponse(status_code=status.HTTP_200_OK, content={})
