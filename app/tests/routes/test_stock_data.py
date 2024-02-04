import os
import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch


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
        var = historical_simulation_var(returns, confidence_level, portfolio_value, historical_days, horizon_days)
    # if var_type == "linear_model":
    #     var = linear_model_var(
    #         returns, confidence_level, portfolio_value, historical_days, horizon_days
    #     )
    # if var_type == "monte_carlo":
    #     var = monte_carlo_var(returns, confidence_level, portfolio_value, horizon_days)

    res = "The VaR at the %.2f confidence level and portfolio value %.2f is %.2f" % (
        confidence_level,
        portfolio_value,
        var,
    )
    return var


def calculate_returns(data: pd.Series) -> pd.Series:
    """Calculate normalized returns."""
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
    """Calculate Value at Risk using historical simulation method."""
    returns_subset: pd.Series = returns[:historical_days]
    sorted_returns = np.sort(returns_subset)
    percentile = 1 - confidence_level
    index = int(percentile * len(sorted_returns))
    worst_portfolio_value = sorted_returns[index] * portfolio_value
    var = (portfolio_value - worst_portfolio_value) * np.sqrt(horizon_days)
    return var


time_index = pd.DatetimeIndex(["2023-08-14", "2023-08-15", "2023-08-16", "2023-08-17", "2023-08-18"])
CLOSE_PRICE_DATA = pd.Series([10, 20, 30, 90, 45], index=time_index)
CLOSE_PRICE_DATA_RETURNS_LIST = [2.0, 1.5, 3.0, 0.5]


def test_calculate_returns():
    returns = calculate_returns(CLOSE_PRICE_DATA)
    returns = returns.tolist()
    assert returns == CLOSE_PRICE_DATA_RETURNS_LIST


time_index = pd.DatetimeIndex(["2023-08-14", "2023-08-15", "2023-08-16", "2023-08-17", "2023-08-18"])
CLOSE_PRICE_DATA_RETURNS = pd.Series([1.1, 1.2, 1.1, 0.9], index=time_index[1:])
HISTORICAL_VAR_PARAMETERS = {
    "returns": CLOSE_PRICE_DATA_RETURNS,
    "confidence_level": 0.99,
    "portfolio_value": 1000000,
    "historical_days": 200,
    "horizon_days": 10,
}
CORRECT_VAR_VALUE = 316227


def test_historical_simulation_var():
    var: float = historical_simulation_var(**HISTORICAL_VAR_PARAMETERS)
    assert int(var) == CORRECT_VAR_VALUE


CORRECT_CALCULATE_VAR_VALUE = 195764


def test_calculate_value_at_risk():
    data_path = os.path.join(os.path.dirname(__file__), "data.csv")
    data = pd.read_csv(data_path)
    var_parameters = {
        "var_type": "historical",
        "data": data,
        "confidence_level": 0.99,
        "portfolio_value": 1000000,
        "historical_days": 200,
        "horizon_days": 10,
    }
    var = calculate_value_at_risk(**var_parameters)
    assert int(var) == CORRECT_CALCULATE_VAR_VALUE
