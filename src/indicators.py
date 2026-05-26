import pandas as pd
import numpy as np


def calculate_returns(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add daily returns to the stock data.
    """

    data = data.copy()
    data["Daily Return"] = data["Close"].pct_change()
    return data


def calculate_moving_averages(data: pd.DataFrame) -> pd.DataFrame:
    """
    Add 20-day and 50-day moving averages.
    """

    data = data.copy()
    data["MA20"] = data["Close"].rolling(window=20).mean()
    data["MA50"] = data["Close"].rolling(window=50).mean()
    return data


def calculate_metrics(data: pd.DataFrame) -> dict:
    """
    Calculate important financial metrics from stock data.
    """

    if data.empty:
        raise ValueError("Data is empty. Cannot calculate metrics.")

    data = calculate_returns(data)
    data = calculate_moving_averages(data)

    latest_close = data["Close"].iloc[-1]

    if len(data) >= 7:
        seven_day_return = (data["Close"].iloc[-1] / data["Close"].iloc[-7] - 1) * 100
    else:
        seven_day_return = np.nan

    if len(data) >= 30:
        thirty_day_return = (data["Close"].iloc[-1] / data["Close"].iloc[-30] - 1) * 100
    else:
        thirty_day_return = np.nan

    daily_volatility = data["Daily Return"].std() * 100

    ma20 = data["MA20"].iloc[-1]
    ma50 = data["MA50"].iloc[-1]

    highest_price = data["Close"].max()
    lowest_price = data["Close"].min()

    return {
        "latest_close": round(latest_close, 2),
        "seven_day_return": round(seven_day_return, 2),
        "thirty_day_return": round(thirty_day_return, 2),
        "daily_volatility": round(daily_volatility, 2),
        "ma20": round(ma20, 2) if not pd.isna(ma20) else "N/A",
        "ma50": round(ma50, 2) if not pd.isna(ma50) else "N/A",
        "highest_price": round(highest_price, 2),
        "lowest_price": round(lowest_price, 2)
    }