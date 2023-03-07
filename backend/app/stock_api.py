from alpha_vantage.timeseries import TimeSeries

from config import settings


api_key = settings.ALPHA_VANTAGE_API_KEY

ts = TimeSeries(api_key, output_format='pandas')
