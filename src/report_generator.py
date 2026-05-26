import os
from datetime import datetime


def generate_rule_based_summary(metrics: dict) -> str:
    seven_day_return = metrics["seven_day_return"]
    thirty_day_return = metrics["thirty_day_return"]

    summary = []

    if seven_day_return > 0:
        summary.append(
            f"The stock showed positive short-term momentum with a 7-day return of {seven_day_return}%."
        )
    elif seven_day_return < 0:
        summary.append(
            f"The stock showed negative short-term movement with a 7-day return of {seven_day_return}%."
        )
    else:
        summary.append("The stock remained almost unchanged over the last 7 trading days.")

    if thirty_day_return > 0:
        summary.append(
            f"Over the last 30 trading days, the stock gained {thirty_day_return}%, indicating a positive monthly trend."
        )
    elif thirty_day_return < 0:
        summary.append(
            f"Over the last 30 trading days, the stock declined by {abs(thirty_day_return)}%, indicating weakness in the monthly trend."
        )
    else:
        summary.append("The stock remained almost flat over the last 30 trading days.")

    if metrics["ma20"] != "N/A" and metrics["ma50"] != "N/A":
        if metrics["ma20"] > metrics["ma50"]:
            summary.append(
                "The 20-day moving average is above the 50-day moving average, which may suggest short-term bullish momentum."
            )
        elif metrics["ma20"] < metrics["ma50"]:
            summary.append(
                "The 20-day moving average is below the 50-day moving average, which may suggest short-term bearish pressure."
            )
        else:
            summary.append(
                "The 20-day and 50-day moving averages are very close, suggesting a neutral trend."
            )

    return " ".join(summary)


def generate_markdown_report(
    ticker: str,
    company_info: dict,
    metrics: dict,
    price_chart_path: str,
    moving_average_chart_path: str,
    financials: dict | None = None,
    financials_summary: str | None = None,
    ai_analysis: str | None = None,
) -> str:
    os.makedirs("reports/markdown", exist_ok=True)
    report_path = f"reports/markdown/{ticker}_report.md"

    summary = generate_rule_based_summary(metrics)

    financials_section = ""

    if financials is not None:
        if financials_summary is None:
            financials_summary = "No financial statement summary available."

        financials_section = f"""
---

## 6. Company Financial Highlights

| Metric | Value |
|---|---:|
| Total Revenue | {financials["total_revenue"]} |
| Net Income | {financials["net_income"]} |
| Total Assets | {financials["total_assets"]} |
| Total Liabilities | {financials["total_liabilities"]} |
| Operating Cash Flow | {financials["operating_cash_flow"]} |
| Free Cash Flow | {financials["free_cash_flow"]} |
| Profit Margin | {financials["profit_margin"]} |
| Debt-to-Assets Ratio | {financials["debt_to_assets"]} |

### Financial Statement Summary

{financials_summary}
"""

    ai_section = ""

    if ai_analysis is not None:
        ai_section = f"""
---

## 7. Local Llama AI-Generated Financial Analysis

{ai_analysis}
"""

    report = f"""# AI Financial Report: {company_info["company_name"]} ({ticker})

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 1. Company Snapshot

| Field | Value |
|---|---|
| Company Name | {company_info["company_name"]} |
| Ticker | {company_info["ticker"]} |
| Sector | {company_info["sector"]} |
| Industry | {company_info["industry"]} |
| Country | {company_info["country"]} |
| Website | {company_info["website"]} |

### Business Summary

{company_info["business_summary"]}

---

## 2. Key Market Metrics

| Metric | Value |
|---|---:|
| Latest Closing Price | ${metrics["latest_close"]} |
| 7-Day Return | {metrics["seven_day_return"]}% |
| 30-Day Return | {metrics["thirty_day_return"]}% |
| Daily Volatility | {metrics["daily_volatility"]}% |
| 20-Day Moving Average | {metrics["ma20"]} |
| 50-Day Moving Average | {metrics["ma50"]} |
| Highest Closing Price in Period | ${metrics["highest_price"]} |
| Lowest Closing Price in Period | ${metrics["lowest_price"]} |

---

## 3. Price Chart

![Price Chart](../../{price_chart_path})

---

## 4. Moving Average Chart

![Moving Average Chart](../../{moving_average_chart_path})

---

## 5. Automated Financial Summary

{summary}

{financials_section}

{ai_section}

---

## 8. Disclaimer

This report is generated automatically using public market data and local AI text generation. It is for educational and informational purposes only and should not be considered financial advice.
"""

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    return report_path