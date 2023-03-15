"""Module contains endpoints for User collection."""
import base64
import requests
from io import BytesIO

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
import pandas as pd
import matplotlib.pyplot as plt
from stock_api import ts
import numpy as np

from schemas.stock import GetStockData


STOCK_DATA_INTERVALS = ['1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly']


router = APIRouter()


def plot_data(data: pd.DataFrame, meta: dict):
    plt.style.use('dark_background')
    fig, ax = plt.subplots()
    L = 6
    x = np.linspace(0, L)
    ncolors = len(plt.rcParams['axes.prop_cycle'])
    shift = np.linspace(0, L, ncolors, endpoint=False)
    for s in shift:
        ax.plot(data['close'])
    ax.set_xlabel('time')
    ax.set_ylabel('value')
    ax.set_title(meta['2. Symbol'])
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    # plt.show()
    return data


def calculate_value_at_risk():
    # TODO
    print("calculate_value_at_risk")


def calculate_hurst_exponent():
    # TODO
    print("calculate_hurst_exponent")

# req_data: dict[Any, Any]
@router.post("/", response_description="Stock data retrieved")
async def get_stock_data(req_data: GetStockData) -> JSONResponse:
    print(req_data)
    data: pd.DataFrame
    meta: dict
    req_data: dict = jsonable_encoder(req_data)
    symbol = req_data['symbol']
    interval = req_data['interval']
    if interval not in STOCK_DATA_INTERVALS:
        raise HTTPException(
            status_code=400, detail="incorrect interval value."
        )
    try:
        if interval == "monthly":
            data, meta = ts.get_monthly(symbol=symbol)
        elif interval == "weekly":
            data, meta = ts.get_weekly(symbol=symbol)
        elif interval == "daily":
            data, meta = ts.get_daily_adjusted(symbol=symbol, outputsize='full')
            data = data[['1. open', '2. high', '3. low', '4. close', '6. volume']]
        else:
            data, meta = ts.get_intraday(symbol=symbol, interval=interval, outputsize='full')
    except ValueError as ex:
        raise HTTPException(
            status_code=400, detail=f"incorrect symbol value. {ex}"
        )
    # Rename columns names and index name
    columns_names = ['open', 'high', 'low', 'close', 'volume']
    data.columns = columns_names
    data['TradeDate'] = data.index.date
    data['time'] = data.index.time
    for statistic in req_data['calculate']:
        if statistic == 'var':
            calculate_value_at_risk()
        if statistic == 'hurst':
            calculate_hurst_exponent()
    # print("dataaaaaaaaaaaaaaaaaaaaa")
    # print(type(data))
    # print(data)
    # print(data.info)
    # print("metaaaaaaaaaaaaaaaaaaaaa")
    # print(type(meta))
    # print(meta)
    image = plot_data(data, meta)
    # data['plot'] = image
    # data = data.to_json()
    return JSONResponse(status_code=status.HTTP_200_OK, content=image)


@router.get("/search", response_description="Stock data retrieved")
async def get_stock_data(symbol: str):
    try:
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={symbol}&apikey=D6Q2O1GZ0MZO4FO0'
        r: requests.Response = requests.get(url)
        data = r.json()
        data = data['bestMatches']
    except KeyError:
        raise HTTPException(
            status_code=400, detail=f"incorrect symbol value."
        )
    for company in data:
        company['symbol'] = company.pop('1. symbol')
        company['name'] = company.pop('2. name')
        company['type'] = company.pop('3. type')
        company['region'] = company.pop('4. region')
        company['marketOpen'] = company.pop('5. marketOpen')
        company['marketClose'] = company.pop('6. marketClose')
        company['timezone'] = company.pop('7. timezone')
        company['currency'] = company.pop('8. currency')
        company['matchScore'] = company.pop('9. matchScore')
    if not data:
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": f"For phrase '{symbol}' company not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=data)
