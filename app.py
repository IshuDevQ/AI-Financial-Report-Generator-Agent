from src.data_fetcher import fetch_stock_data, fetch_company_info
from src.indicators import calculate_returns, calculate_moving_averages, calculate_metrics
from src.charts import create_price_chart, create_moving_average_chart
from src.report_generator import generate_markdown_report
from src.pdf_generator import generate_pdf_report
from src.financials_fetcher import fetch_company_financials, generate_financials_summary
from src.local_ai_writer import generate_local_ai_financial_analysis
from src.utils import ensure_directories_exist


def run_financial_report_agent(ticker: str, period: str = "6mo") -> None:
    """
    Run the complete financial report generation pipeline.
    """

    ticker = ticker.upper().strip()

    print(f"\nStarting financial report generation for {ticker}...\n")

    ensure_directories_exist()

    print("Fetching stock data...")
    stock_data = fetch_stock_data(ticker, period)

    print("Fetching company information...")
    company_info = fetch_company_info(ticker)

    print("Calculating indicators and metrics...")
    stock_data = calculate_returns(stock_data)
    stock_data = calculate_moving_averages(stock_data)
    metrics = calculate_metrics(stock_data)

    print("Fetching company financial statements...")
    financials = fetch_company_financials(ticker)

    print("Generating financial statement summary...")
    financials_summary = generate_financials_summary(financials)

    print("Creating charts...")
    price_chart_path = create_price_chart(stock_data, ticker)
    moving_average_chart_path = create_moving_average_chart(stock_data, ticker)

    print("Generating local AI financial analysis using Ollama...")
    ai_analysis = generate_local_ai_financial_analysis(
        ticker=ticker,
        company_info=company_info,
        metrics=metrics,
        financials=financials,
        model="llama3.2:3b",
    )

    print("Generating Markdown report...")
    markdown_report_path = generate_markdown_report(
        ticker=ticker,
        company_info=company_info,
        metrics=metrics,
        price_chart_path=price_chart_path,
        moving_average_chart_path=moving_average_chart_path,
        financials=financials,
        financials_summary=financials_summary,
        ai_analysis=ai_analysis,
    )

    print("Generating PDF report...")
    pdf_report_path = generate_pdf_report(
        ticker=ticker,
        company_info=company_info,
        metrics=metrics,
        price_chart_path=price_chart_path,
        moving_average_chart_path=moving_average_chart_path,
        financials=financials,
        financials_summary=financials_summary,
        ai_analysis=ai_analysis,
    )

    print("\nReport generated successfully!")
    print(f"Markdown report: {markdown_report_path}")
    print(f"PDF report: {pdf_report_path}")
    print(f"Price chart: {price_chart_path}")
    print(f"Moving average chart: {moving_average_chart_path}")


if __name__ == "__main__":
    ticker = input("Enter stock ticker, for example AAPL, MSFT, TSLA: ")
    period = input(
        "Enter period, for example 1mo, 3mo, 6mo, 1y. Press Enter for default 6mo: "
    )

    if period.strip() == "":
        period = "6mo"

    run_financial_report_agent(ticker, period)