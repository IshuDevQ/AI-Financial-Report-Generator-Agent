import os
import matplotlib.pyplot as plt
import pandas as pd


def create_price_chart(data: pd.DataFrame, ticker: str) -> str:
    """
    Create a stock closing price chart.
    """

    os.makedirs("charts", exist_ok=True)

    chart_path = f"charts/{ticker}_price_chart.png"

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Close"], label="Close Price")
    plt.title(f"{ticker} Stock Closing Price")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path


def create_moving_average_chart(data: pd.DataFrame, ticker: str) -> str:
    """
    Create a chart showing closing price, 20-day MA, and 50-day MA.
    """

    os.makedirs("charts", exist_ok=True)

    chart_path = f"charts/{ticker}_moving_average_chart.png"

    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["Close"], label="Close Price")

    if "MA20" in data.columns:
        plt.plot(data.index, data["MA20"], label="20-Day Moving Average")

    if "MA50" in data.columns:
        plt.plot(data.index, data["MA50"], label="50-Day Moving Average")

    plt.title(f"{ticker} Moving Average Analysis")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return chart_path