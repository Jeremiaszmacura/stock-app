"""Module contains endpoints for User collection."""
import base64
import requests
import json
import datetime
import os
from io import BytesIO
import matplotlib
from pprint import pprint

import numpy as np
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
import pandas as pd
import matplotlib.pyplot as plt
from stock_api import ts
import numpy as np
from scipy.stats import norm
from pydantic import parse_obj_as

from schemas.stock import GetStockData, GetPortfolioData
from schemas.user import UserOut
from security import oauth2_scheme, get_current_user
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
    # print(data)
    # data["TradeDate"] = data.index
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
    returns = data / data.shift(-1)
    returns = returns.dropna()
    return returns


def calculate_log_returns(data: pd.Series) -> pd.Series:
    """Calculate normalized log returns."""
    returns = np.log10(data) / np.log10(data.shift(1))
    returns = returns.dropna()
    return returns


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def portfolio_historical_var(
    portfolio_with_data: dict,
    confidence_level: float,
    horizon_days: int,
    date_from: datetime.date,
    date_to: datetime.date
) -> float:
    # calculate returns
    # TODO (probably): move out of this function and you don't need to pass prices then, just returns to this function
    for symbol_data in portfolio_with_data.values():
        data = symbol_data["data"]
        close_prices: pd.Series = data["close"]
        returns: pd.Series = calculate_returns(close_prices)
        symbol_data["returns"] = returns

    portfolio_values = pd.Series()
    for day in daterange(date_from, date_to + datetime.timedelta(1)):
        pd_day = pd.Timestamp(day)
        portfolio_value = 0
        include_date = True
        for symbol, symbol_data in portfolio_with_data.items():
            value = symbol_data["value"]
            returns: pd.Series = symbol_data["returns"]
            if pd_day in returns:
                portfolio_value += value*returns[pd_day]
            else:
                include_date = False
                break
        if include_date:
            # print(portfolio_value)
            portfolio_values[pd_day] = portfolio_value
            
    sorted_portfolio_values = np.sort(portfolio_values)
    print(sorted_portfolio_values)
    percentile = 1 - confidence_level
    percentile_sample_index = int(percentile * len(sorted_portfolio_values))
    worst_portfolio_value = sorted_portfolio_values[percentile_sample_index]
    current_portfolio_value = sum(symbol_data["value"] for symbol_data in portfolio_with_data.values())
    print(f"current_value={current_portfolio_value}")
    var = (current_portfolio_value - worst_portfolio_value) * np.sqrt(horizon_days)
    print(portfolio_value)
    print(worst_portfolio_value)
    print(horizon_days)
    print(var)


            
    
    # for company in portfolio_with_data:
    #     data: pd.DataFrame = company["data"]
    #     close_prices: pd.Series = data["close"]
    #     returns: pd.Series = calculate_returns(close_prices)
    #     most_recent_price: float = close_prices.values[0]
    #     historically_simulated_prices = []
    #     for signle_return in returns:
    #         historically_simulated_prices.append(most_recent_price*signle_return)
        


def historical_simulation_var(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: int | float,
    historical_days: int,
    horizon_days: int,
) -> float:
    """Calculate Value at Risk using historical simulation method."""
    first_return = max(len(returns) - historical_days, 0)
    returns_subset: pd.Series = returns[first_return:]
    sorted_returns = np.sort(returns_subset)    
    print(sorted_returns*100)
    percentile = 1 - confidence_level
    percentile_sample_index = int(percentile * len(sorted_returns))
    worst_portfolio_value = sorted_returns[percentile_sample_index] * portfolio_value
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
    first_return = max(len(returns) - historical_days, 0)
    returns_subset: pd.Series = returns[first_return:]
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
    number_of_samples: int = 5000
) -> float:
    """Calculate Value at Risk using monte carlo simulation."""
    first_return = max(len(returns) - historical_days, 0)
    returns_subset: pd.Series = returns[first_return:]
    std_dev = np.std(returns_subset)
    # loc=Mean(center), scale=Std(Spread/Width)
    norm_distribution_samples = np.random.normal(loc=0, scale=std_dev, size=number_of_samples)
    sorted_norm_distribution_samples = np.sort(norm_distribution_samples)    
    percentile = 1 - confidence_level
    percentile_sample_index = int(percentile * len(sorted_norm_distribution_samples))
    one_day_var = portfolio_value * sorted_norm_distribution_samples[percentile_sample_index]
    var = abs(one_day_var * np.sqrt(horizon_days))
    return var


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
    if var_type == "monte_carlo":
        var = monte_carlo_var(
            returns, confidence_level, portfolio_value, historical_days, horizon_days
        )

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
    # data_path = os.path.join(os.path.dirname(__file__), "samsung_pand.csv")
    # data = pd.read_csv(data_path, index_col='date')
    # meta = {"2. Symbol": "xd"}
    # print(data)
    data = prepare_data(data, interval)

    # adjust selected datetime
    date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
    print(f"Data from: {date_from} to {date_to}")
    mask = (data["TradeDate"] >= date_from) & (data["TradeDate"] <= date_to)
    data = data.loc[mask]
    # print("hihihihi")
    # print(data)
    # data.to_csv("wtf", sep=',')
    # print(len(data.index))
    
    if "var" in req_data["calculate"]:
        var_type = req_data["var_type"]
        portfolio_value = req_data["portfolio_value"]
        confidence_level = req_data["confidence_level"]
        horizon_days = req_data["horizon_days"]
        if len(data) < req_data["historical_days"]:
            historical_days = len(data)
        else:
            historical_days = req_data["historical_days"]  

    plot = plot_data(plot_type, data, meta, name, interval)
    res_data = {"plot": plot}
    data.to_csv("file_name.csv", encoding="utf-8")
    for statistic in req_data["calculate"]:
        if statistic == "var":
            var = calculate_value_at_risk(
                var_type, data, confidence_level, portfolio_value, historical_days, horizon_days
            )
            res_data["var"] = var
            res_data["historical_days"] = historical_days
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


@router.post("/portfolio-var", response_description="Stock data retrieved")
async def calculate_portfolio_var(
    req_data: GetPortfolioData, token: str = Depends(oauth2_scheme)
) -> JSONResponse:
    req_data: dict = jsonable_encoder(req_data)
    print(req_data)
    var_type = req_data["var_type"]
    confidence_level = req_data["confidence_level"]
    horizon_days = req_data["horizon_days"]
    portfolio = req_data["portfolio"]
    date_from = req_data["date_from"]
    date_to = req_data["date_to"]
    portfolio_with_data = {}
    historical_days_list = []
    date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
    date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
    print(portfolio)
    # Get data for each portfolio item
    for company in portfolio:
        try:
            data, meta = ts.get_daily_adjusted(symbol=company["symbol"], outputsize="full")
            data = prepare_data(data, interval="daily")
            # adjust selected datetime
            print(f"Data from: {date_from} to {date_to}")
            mask = (data["TradeDate"] >= date_from) & (data["TradeDate"] <= date_to)
            data = data.loc[mask]
            historical_days_list.append(len(data))
            portfolio_with_data[company["symbol"]] = {
                "value": company["value"],
                "data": data,
            }
            # portfolio_with_data.append({
            #     "symbol": company["symbol"],
            #     "value": company["value"],
            #     "data": data,
            #     "meta": meta
            # })
        except ValueError as ex:
            raise HTTPException(status_code=400, detail=f"incorrect symbol value. {ex}")
    print(portfolio_with_data)
    historical_days = round(sum(historical_days_list)/len(historical_days_list))
    print(f"Historical Days: {historical_days}")
    if var_type == "historical":
        var = portfolio_historical_var(portfolio_with_data, confidence_level, horizon_days, date_from, date_to)
    
    var = 10
    res_data = {"var": var, "historical_days": historical_days}
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
