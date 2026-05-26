import requests


def build_local_ai_prompt(
    ticker: str,
    company_info: dict,
    metrics: dict,
    financials: dict,
) -> str:
    """
    Build a structured prompt for the local Llama model.

    The model should only explain the data provided.
    It should not invent numbers or give investment advice.
    """

    prompt = f"""
You are a financial analysis assistant.

Write a clear, professional financial analysis for the company below.

Rules:
1. Use only the data provided.
2. Do not invent numbers.
3. Do not give buy, sell, or hold advice.
4. Do not make guaranteed predictions.
5. Explain trends in simple, professional language.
6. Keep the tone educational.
7. Mention that this is not financial advice.

Company Information:
Company Name: {company_info.get("company_name", "N/A")}
Ticker: {ticker}
Sector: {company_info.get("sector", "N/A")}
Industry: {company_info.get("industry", "N/A")}
Country: {company_info.get("country", "N/A")}

Stock Metrics:
Latest Closing Price: ${metrics.get("latest_close", "N/A")}
7-Day Return: {metrics.get("seven_day_return", "N/A")}%
30-Day Return: {metrics.get("thirty_day_return", "N/A")}%
Daily Volatility: {metrics.get("daily_volatility", "N/A")}%
20-Day Moving Average: {metrics.get("ma20", "N/A")}
50-Day Moving Average: {metrics.get("ma50", "N/A")}
Highest Closing Price in Period: ${metrics.get("highest_price", "N/A")}
Lowest Closing Price in Period: ${metrics.get("lowest_price", "N/A")}

Company Financial Highlights:
Total Revenue: {financials.get("total_revenue", "N/A")}
Net Income: {financials.get("net_income", "N/A")}
Total Assets: {financials.get("total_assets", "N/A")}
Total Liabilities: {financials.get("total_liabilities", "N/A")}
Operating Cash Flow: {financials.get("operating_cash_flow", "N/A")}
Free Cash Flow: {financials.get("free_cash_flow", "N/A")}
Profit Margin: {financials.get("profit_margin", "N/A")}
Debt-to-Assets Ratio: {financials.get("debt_to_assets", "N/A")}

Write the response using exactly these headings:

Executive Summary
Stock Performance Analysis
Moving Average Analysis
Financial Statement Analysis
Risk Considerations
Educational Disclaimer

Keep the analysis concise and useful.
"""

    return prompt


def generate_local_ai_financial_analysis(
    ticker: str,
    company_info: dict,
    metrics: dict,
    financials: dict,
    model: str = "llama3.2:3b",
) -> str:
    """
    Generate financial analysis using a local Ollama Llama model.

    Ollama must be running locally.
    Default Ollama API endpoint:
    http://localhost:11434/api/generate
    """

    prompt = build_local_ai_prompt(
        ticker=ticker,
        company_info=company_info,
        metrics=metrics,
        financials=financials,
    )

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,
            "num_predict": 700,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()

        result = response.json()
        ai_text = result.get("response", "").strip()

        if not ai_text:
            return (
                "Local AI analysis could not be generated because the model returned "
                "an empty response."
            )

        return ai_text

    except requests.exceptions.ConnectionError:
        return (
            "Local AI analysis could not be generated because Ollama is not running. "
            "Open terminal and run: ollama serve"
        )

    except requests.exceptions.Timeout:
        return (
            "Local AI analysis could not be generated because the Ollama request timed out. "
            "Try again or use a smaller model."
        )

    except Exception as error:
        return f"Local AI analysis could not be generated due to an error: {error}"