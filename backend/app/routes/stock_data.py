"""Module contains endpoints for User collection."""
import base64
import requests
import json
import datetime
from io import BytesIO
from typing import Annotated
import matplotlib

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
    """Preparation of retrieved data from api for search result."""
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
    """Preparation of retrieved data from api for further calculations and plotting."""
    if interval == "daily":
        data = data[["1. open", "2. high", "3. low", "4. close", "6. volume"]]
    # Rename columns names and index name
    columns_names = ["open", "high", "low", "close", "volume"]
    data.columns = columns_names
    data["TradeDate"] = data.index.date
    data["time"] = data.index.time
    return data


def linear_plot(data: pd.DataFrame, ax: matplotlib.axes.Axes):
    shift = np.linspace(0, 6)
    for _ in shift:
        ax.plot(data["close"], color="#00ccff", linewidth=0.5)


def candle_stick_plot(data: pd.DataFrame):
    plt.subplots_adjust(bottom=0.20)
    plt.xticks(rotation=70, fontsize=6)
    plt.yticks(fontsize=8)
    up = data[data.close >= data["open"]]
    down = data[data["close"] < data["open"]]
    up_color = "#89ff00"
    up_shadow_color = "#4CAE50"
    down_color = "#ff005e"
    down_shadow_color = "#9C2525"
    bar_width = 0.5
    shadow_width = 0.2
    # Plotting up prices of the stock
    plt.bar(up.index, up.close - up.open, bar_width, bottom=up.open, color=up_color)
    plt.bar(up.index, up.high - up.close, shadow_width, bottom=up.close, color=up_shadow_color)
    plt.bar(up.index, up.low - up.open, shadow_width, bottom=up.open, color=up_shadow_color)
    # Plotting down prices of the stock
    plt.bar(down.index, down.close - down.open, bar_width, bottom=down.open, color=down_color)
    plt.bar(
        down.index, down.high - down.open, shadow_width, bottom=down.open, color=down_shadow_color
    )
    plt.bar(
        down.index, down.low - down.close, shadow_width, bottom=down.close, color=down_shadow_color
    )


def plot_data(plot_type: str, data: pd.DataFrame, meta: dict, name: str, frequency: str):
    """Plot charts based on stock market data."""
    plt.style.use("dark_background")
    fig, ax = plt.subplots()
    plt.rc("font", size=8)
    if frequency not in ["daily", "weekly", "monthly"]:
        plt.subplots_adjust(bottom=0.20)
        plt.xticks(rotation=70, fontsize=6)
    if plot_type == "linear":
        linear_plot(data, ax)
    elif plot_type == "candlestick":
        candle_stick_plot(data)
    ax.set_xlabel("time", fontsize=12, labelpad=6, fontweight="bold")
    ax.set_ylabel("value", fontsize=12, labelpad=6, fontweight="bold")
    ax.set_title(f'{meta["2. Symbol"]} ({name})', fontsize=14, pad=12, fontweight="bold")
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=300)
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def calculate_returns(data: pd.Series) -> pd.Series:
    """Calculate normalized returns."""
    print(data.index)
    returns = data / data.shift(1)
    returns = returns.dropna()
    return returns


def calculate_log_returns(data: pd.Series) -> pd.Series:
    """Calculate normalized log returns."""
    returns = np.log10(data) / np.log10(data.shift(1))
    returns = returns.dropna()
    return returns


def historical_simulation_var(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
) -> float:
    """Calculate Value at Risk using historical simulation method."""
    returns_subset: pd.Series = returns[:historical_days]
    sorted_returns = np.sort(returns_subset)
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
    """Calculate Value at Risk using linear model simulation."""
    returns_subset: pd.Series = returns[:historical_days]
    # Standard deviation is the statistical measure of market volatility
    std_dev = np.std(returns_subset)
    standard_score = norm.ppf(confidence_level)
    var = standard_score * std_dev * portfolio_value * np.sqrt(horizon_days)
    return var


def monte_carlo_var(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
) -> float:
    """Calculate Value at Risk using monte carlo simulation."""
    pass


def calculate_value_at_risk(
    var_type: str,
    data: pd.DataFrame,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
):
    """Calcualte Value at Risk."""
    data = data["close"]
    returns = calculate_returns(data)
    # returns = calculate_log_returns(data)

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
async def calculate_stock_data(
    req_data: GetStockData, token: str = Depends(oauth2_scheme)
) -> JSONResponse:
    """Endpoint to get data and calculate statistics for specified company."""
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
    symbol = req_data["symbol"]
    name = req_data["name"]
    interval = req_data["interval"]
    date_from = req_data["date_from"]
    date_to = req_data["date_to"]
    plot_type = req_data["plot_type"]
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

    # adjust selected datetime
    date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
    mask = (data["TradeDate"] > date_from) & (data["TradeDate"] <= date_to)
    data = data.loc[mask]

    plot = plot_data(plot_type, data, meta, name, interval)
    res_data = {"plot": plot}
    data.to_csv("file_name.csv", encoding="utf-8")
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
        user["analysis_history"].append(analysed)
        await user_crud.update_user(user["_id"], user)

    res_data = json.dumps(res_data)
    return JSONResponse(status_code=status.HTTP_200_OK, content=res_data)


@router.get("/search", response_description="Stock data retrieved")
async def search_stock_data(symbol: str, token: str = Depends(oauth2_scheme)):
    """Endpoint to search for company based on a given phrase."""
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

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"data": data, "user_availability": user_availability},
    )
