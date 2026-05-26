import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker: str, period: str = "6mo") -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol, for example AAPL, MSFT, TSLA.
    period : str
        Time period for historical data. Examples: 1mo, 3mo, 6mo, 1y, 5y.

    Returns
    -------
    pd.DataFrame
        Historical stock price data.
    """

    ticker = ticker.upper().strip()

    stock = yf.Ticker(ticker)
    data = stock.history(period=period)

    if data.empty:
        raise ValueError(f"No stock data found for ticker: {ticker}")

    return data


def fetch_company_info(ticker: str) -> dict:
    """
    Fetch company information using yfinance.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol.

    Returns
    -------
    dict
        Company information such as name, sector, industry, and summary.
    """

    ticker = ticker.upper().strip()

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker,
        "company_name": info.get("longName", ticker),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "country": info.get("country", "N/A"),
        "website": info.get("website", "N/A"),
        "business_summary": info.get("longBusinessSummary", "No summary available.")
    }