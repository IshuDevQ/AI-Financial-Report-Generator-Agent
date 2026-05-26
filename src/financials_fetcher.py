import yfinance as yf
import pandas as pd


def format_large_number(value):
    """
    Format large financial numbers into readable units.
    """

    if value is None or pd.isna(value):
        return "N/A"

    value = float(value)

    if abs(value) >= 1_000_000_000_000:
        return f"${value / 1_000_000_000_000:.2f}T"
    elif abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    else:
        return f"${value:,.2f}"


def get_latest_value(statement: pd.DataFrame, possible_rows: list[str]):
    """
    Get the latest available value from a financial statement.

    yfinance financial statements are usually stored with:
    - rows as financial metrics
    - columns as dates
    """

    if statement is None or statement.empty:
        return None

    for row in possible_rows:
        if row in statement.index:
            return statement.loc[row].iloc[0]

    return None


def fetch_company_financials(ticker: str) -> dict:
    """
    Fetch company financial statement highlights using yfinance.
    """

    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    income_statement = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow

    total_revenue = get_latest_value(
        income_statement,
        ["Total Revenue", "Operating Revenue"]
    )

    net_income = get_latest_value(
        income_statement,
        ["Net Income", "Net Income Common Stockholders"]
    )

    total_assets = get_latest_value(
        balance_sheet,
        ["Total Assets"]
    )

    total_liabilities = get_latest_value(
        balance_sheet,
        ["Total Liabilities Net Minority Interest", "Total Liab"]
    )

    operating_cash_flow = get_latest_value(
        cash_flow,
        ["Operating Cash Flow", "Total Cash From Operating Activities"]
    )

    free_cash_flow = get_latest_value(
        cash_flow,
        ["Free Cash Flow"]
    )

    profit_margin = None
    if total_revenue and net_income:
        profit_margin = (net_income / total_revenue) * 100

    debt_to_assets = None
    if total_assets and total_liabilities:
        debt_to_assets = (total_liabilities / total_assets) * 100

    return {
        "total_revenue": format_large_number(total_revenue),
        "net_income": format_large_number(net_income),
        "total_assets": format_large_number(total_assets),
        "total_liabilities": format_large_number(total_liabilities),
        "operating_cash_flow": format_large_number(operating_cash_flow),
        "free_cash_flow": format_large_number(free_cash_flow),
        "profit_margin": f"{profit_margin:.2f}%" if profit_margin is not None else "N/A",
        "debt_to_assets": f"{debt_to_assets:.2f}%" if debt_to_assets is not None else "N/A",
    }


def generate_financials_summary(financials: dict) -> str:
    """
    Generate a simple financial statement summary.
    """

    summary = []

    revenue = financials.get("total_revenue", "N/A")
    net_income = financials.get("net_income", "N/A")
    profit_margin = financials.get("profit_margin", "N/A")
    debt_to_assets = financials.get("debt_to_assets", "N/A")
    free_cash_flow = financials.get("free_cash_flow", "N/A")

    if revenue != "N/A":
        summary.append(
            f"The company reported total revenue of {revenue} in the latest available annual financial statement."
        )

    if net_income != "N/A":
        summary.append(
            f"Net income stood at {net_income}, showing the company's bottom-line profitability."
        )

    if profit_margin != "N/A":
        summary.append(
            f"The profit margin was approximately {profit_margin}, which helps evaluate how efficiently revenue is converted into profit."
        )

    if free_cash_flow != "N/A":
        summary.append(
            f"Free cash flow was {free_cash_flow}, which is important because it shows cash available after capital expenditures."
        )

    if debt_to_assets != "N/A":
        summary.append(
            f"The debt-to-assets ratio was approximately {debt_to_assets}, giving a basic view of the company's balance sheet leverage."
        )

    if not summary:
        return "Financial statement data was not available for this ticker."

    return " ".join(summary)