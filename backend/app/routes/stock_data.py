"""Module contains endpoints for User collection."""
import base64
import requests
import json
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
import pandas as pd
import matplotlib.pyplot as plt
from stock_api import ts
import numpy as np
from scipy.stats import norm
from pydantic import parse_obj_as

from schemas.stock import GetStockData
from schemas.user import UserOut, UserCreate, UserUpdate
from security import get_current_active_user, oauth2_scheme, get_current_user
from crud import user_crud


STOCK_DATA_INTERVALS = ["1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"]


router = APIRouter()
pd.options.mode.chained_assignment = None


def prepare_search_data(data: list[dict]) -> list[dict]:
    for company in data:
        company["symbol"] = company.pop("1. symbol")
        company["name"] = company.pop("2. name")
        company["type"] = company.pop("3. type")
        company["region"] = company.pop("4. region")
        company["marketOpen"] = company.pop("5. marketOpen")
        company["marketClose"] = company.pop("6. marketClose")
        company["timezone"] = company.pop("7. timezone")
        company["currency"] = company.pop("8. currency")
        company["matchScore"] = company.pop("9. matchScore")
    return data


def prepare_data(data: pd.DataFrame, interval: str) -> pd.DataFrame:
    if interval == "daily":
        data = data[["1. open", "2. high", "3. low", "4. close", "6. volume"]]
    # Rename columns names and index name
    columns_names = ["open", "high", "low", "close", "volume"]
    data.columns = columns_names
    data["TradeDate"] = data.index.date
    data["time"] = data.index.time
    return data


def plot_data(data: pd.DataFrame, meta: dict):
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    L = 6
    x = np.linspace(0, L)
    ncolors = len(plt.rcParams["axes.prop_cycle"])
    shift = np.linspace(0, L, ncolors, endpoint=False)
    for s in shift:
        ax.plot(data["close"])
    ax.set_xlabel("time")
    ax.set_ylabel("value")
    ax.set_title(meta["2. Symbol"])
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # plt.show()
    return data


def calculate_returns(data: pd.Series) -> pd.Series:
    returns = data / data.shift(1)
    returns = returns.dropna()
    return returns


def historical_simulation_var(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
) -> float:
    sorted_returns = np.sort(returns)
    percentile = 1 - confidence_level
    index = int(percentile * len(sorted_returns))
    worst_portfolio_value = sorted_returns[index] * portfolio_value
    var = (portfolio_value - worst_portfolio_value) * np.sqrt(horizon_days)
    return var


def linear_model_var(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
) -> float:
    # Standard deviation is the statistical measure of market volatility
    std_dev = np.std(returns)
    quantile = norm.ppf(confidence_level)
    var = quantile * std_dev * portfolio_value * np.sqrt(horizon_days)
    return var


def monte_carlo_var(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
) -> float:
    pass


def calculate_value_at_risk(
    var_type: str,
    data: pd.DataFrame,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
):
    data = data["close"]
    returns = calculate_returns(data)

    if var_type == "historical":
        var = historical_simulation_var(
            returns, confidence_level, portfolio_value, historical_days, horizon_days
        )
    if var_type == "linear_model":
        var = linear_model_var(
            returns, confidence_level, portfolio_value, historical_days, horizon_days
        )
    # if var_type == "monte_carlo":
    #     var = monte_carlo_var(returns, confidence_level, portfolio_value, horizon_days)

    res = "The VaR at the %.2f confidence level and portfolio value %.2f is %.2f" % (
        confidence_level,
        portfolio_value,
        var,
    )
    return var


def calculate_hurst_exponent():
    # TODO
    print("calculate_hurst_exponent")


@router.post("/", response_description="Stock data retrieved")
async def get_stock_data(req_data: GetStockData, token: str = Depends(oauth2_scheme)) -> JSONResponse:
    # Check if user is logged in
    user = None
    try:
        user = await get_current_user(token)
    except HTTPException as error:
        if error.status_code == 401:
            user_availability = False
        else:
            user_availability = True
    
    data: pd.DataFrame
    meta: dict
    req_data: dict = jsonable_encoder(req_data)
    print(req_data)
    symbol = req_data["symbol"]
    interval = req_data["interval"]
    if "var" in req_data["calculate"]:
        var_type = req_data["var_type"]
        portfolio_value = req_data["portfolio_value"]
        confidence_level = req_data["confidence_level"]
        historical_days = req_data["historical_days"]
        horizon_days = req_data["horizon_days"]

    if interval not in STOCK_DATA_INTERVALS:
        raise HTTPException(status_code=400, detail="incorrect interval value.")
    try:
        if interval == "monthly":
            data, meta = ts.get_monthly(symbol=symbol)
        elif interval == "weekly":
            data, meta = ts.get_weekly(symbol=symbol)
        elif interval == "daily":
            data, meta = ts.get_daily_adjusted(symbol=symbol, outputsize="full")
        else:
            data, meta = ts.get_intraday(symbol=symbol, interval=interval, outputsize="full")
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=f"incorrect symbol value. {ex}")
    data = prepare_data(data, interval)
    plot = plot_data(data, meta)
    res_data = {"plot": plot}
    for statistic in req_data["calculate"]:
        if statistic == "var":
            var = calculate_value_at_risk(
                var_type, data, confidence_level, portfolio_value, historical_days, horizon_days
            )
            res_data["var"] = var
        if statistic == "hurst":
            calculate_hurst_exponent()
    
    # Add Analyse data to history of current loged in user
    if user:
        user = jsonable_encoder(parse_obj_as(UserOut, user))
        analysed: dict = req_data | res_data
        print(user)
        print(type(user))
        print(type(user["analysis_history"]))
        user["analysis_history"].append(analysed)
        await user_crud.update_user(user["_id"], user)    
    
    res_data = json.dumps(res_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=res_data)


@router.get("/search", response_description="Stock data retrieved")
async def get_stock_data(symbol: str, token: str = Depends(oauth2_scheme)):
    user = None
    try:
        user = await get_current_user(token)
    except HTTPException as error:
        if error.status_code == 401:
            user_availability = False
    if user:
        user_availability = True
    
    try:
        url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey=D6Q2O1GZ0MZO4FO0"
        r: requests.Response = requests.get(url)
        data: dict = r.json()
        data: list = data["bestMatches"]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"incorrect symbol value.")
    
    if not data:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": f"For phrase '{symbol}' company not found"},
        )
    data: list[dict] = prepare_search_data(data)
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"data": data, "user_availability": user_availability})
