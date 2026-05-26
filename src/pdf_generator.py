import os
import re
from datetime import datetime
from fpdf import FPDF


PRIMARY = (31, 41, 55)
MUTED = (90, 98, 110)
LIGHT_BG = (245, 247, 250)
BORDER = (210, 214, 220)
SUCCESS = (22, 122, 73)
DANGER = (180, 54, 54)


class FinancialReportPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_margins(14, 16, 14)
        self.set_auto_page_break(auto=True, margin=16)
        self.alias_nb_pages()
        self.report_title = "AI Financial Report"

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*MUTED)
        self.cell(0, 6, self.report_title, ln=True, align="R")

        self.set_draw_color(*BORDER)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-12)
        self.set_draw_color(*BORDER)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())

        self.ln(2)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*MUTED)
        self.cell(0, 6, f"Page {self.page_no()} of {{nb}}", align="C")


def clean_text(text) -> str:
    if text is None:
        return "N/A"

    return (
        str(text)
        .replace("—", "-")
        .replace("–", "-")
        .replace("’", "'")
        .replace("‘", "'")
        .replace("“", '"')
        .replace("”", '"')
        .replace("•", "-")
        .replace("₹", "Rs.")
        .replace("\u2011", "-")
    )


def strip_markdown(text: str) -> str:
    text = clean_text(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    return text.strip()


def parse_ai_sections(ai_analysis: str) -> list[tuple[str, str]]:
    text = clean_text(ai_analysis).strip()

    headings = [
        "Executive Summary",
        "Stock Performance Analysis",
        "Moving Average Analysis",
        "Financial Statement Analysis",
        "Risk Considerations",
        "Educational Disclaimer",
    ]

    sections = []

    for index, heading in enumerate(headings):
        pattern = rf"(?:\*\*)?{re.escape(heading)}(?:\*\*)?"
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if not match:
            continue

        start = match.end()
        end = len(text)

        for next_heading in headings[index + 1:]:
            next_pattern = rf"(?:\*\*)?{re.escape(next_heading)}(?:\*\*)?"
            next_match = re.search(next_pattern, text[start:], flags=re.IGNORECASE)

            if next_match:
                end = start + next_match.start()
                break

        body = strip_markdown(text[start:end]).strip()

        if body:
            sections.append((heading, body))

    if sections:
        return sections

    return [("AI Analysis", strip_markdown(text))]


def add_title_page_header(
    pdf: FinancialReportPDF,
    company_info: dict,
    ticker: str,
) -> None:
    pdf.set_fill_color(*PRIMARY)
    pdf.rect(0, 0, pdf.w, 38, style="F")

    pdf.set_xy(14, 11)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 10, "AI Financial Report", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 12)
    company_name = clean_text(company_info.get("company_name", ticker))
    pdf.cell(0, 8, f"{company_name} ({ticker})", ln=True)

    pdf.set_x(14)
    pdf.set_font("Helvetica", "", 9)
    generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf.cell(0, 6, f"Generated on {generated_time}", ln=True)

    pdf.set_y(46)


def add_section_title(pdf: FPDF, title: str) -> None:
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(*PRIMARY)
    pdf.cell(0, 8, clean_text(title), ln=True)

    pdf.set_draw_color(*BORDER)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(4)


def add_subsection_title(pdf: FPDF, title: str) -> None:
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_text_color(*PRIMARY)
    pdf.cell(0, 7, clean_text(title), ln=True)
    pdf.ln(1)


def add_paragraph(
    pdf: FPDF,
    text: str,
    font_size: int = 10,
    line_height: float = 5.7,
) -> None:
    pdf.set_font("Helvetica", "", font_size)
    pdf.set_text_color(45, 52, 60)

    cleaned = strip_markdown(text)
    paragraphs = [p.strip() for p in cleaned.split("\n") if p.strip()]

    for paragraph in paragraphs:
        pdf.multi_cell(0, line_height, paragraph)
        pdf.ln(1.5)

    pdf.ln(1)


def add_info_grid(pdf: FPDF, company_info: dict) -> None:
    rows = [
        ("Company", company_info.get("company_name", "N/A")),
        ("Ticker", company_info.get("ticker", "N/A")),
        ("Sector", company_info.get("sector", "N/A")),
        ("Industry", company_info.get("industry", "N/A")),
        ("Country", company_info.get("country", "N/A")),
        ("Website", company_info.get("website", "N/A")),
    ]

    left_x = pdf.get_x()
    start_y = pdf.get_y()
    col_width = (pdf.w - pdf.l_margin - pdf.r_margin) / 2
    box_height = 13

    for i, (label, value) in enumerate(rows):
        x = left_x + (i % 2) * col_width
        y = start_y + (i // 2) * box_height

        pdf.set_xy(x, y)
        pdf.set_fill_color(*LIGHT_BG)
        pdf.set_draw_color(*BORDER)
        pdf.rect(x, y, col_width - 3, box_height - 2, style="DF")

        pdf.set_xy(x + 3, y + 2)
        pdf.set_font("Helvetica", "B", 8)
        pdf.set_text_color(*MUTED)
        pdf.cell(col_width - 8, 4, label.upper(), ln=True)

        pdf.set_x(x + 3)
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*PRIMARY)
        pdf.cell(col_width - 8, 5, clean_text(value)[:44], ln=True)

    pdf.set_y(start_y + 3 * box_height + 2)


def add_metric_cards(pdf: FPDF, metrics: dict) -> None:
    cards = [
        ("Latest Close", f"${metrics['latest_close']}", PRIMARY),
        (
            "7-Day Return",
            f"{metrics['seven_day_return']}%",
            SUCCESS if metrics["seven_day_return"] >= 0 else DANGER,
        ),
        (
            "30-Day Return",
            f"{metrics['thirty_day_return']}%",
            SUCCESS if metrics["thirty_day_return"] >= 0 else DANGER,
        ),
        ("Daily Volatility", f"{metrics['daily_volatility']}%", PRIMARY),
    ]

    card_gap = 4
    card_width = (pdf.w - pdf.l_margin - pdf.r_margin - 3 * card_gap) / 4
    card_height = 20
    start_x = pdf.get_x()
    y = pdf.get_y()

    for i, (label, value, color) in enumerate(cards):
        x = start_x + i * (card_width + card_gap)

        pdf.set_fill_color(*LIGHT_BG)
        pdf.set_draw_color(*BORDER)
        pdf.rect(x, y, card_width, card_height, style="DF")

        pdf.set_xy(x + 3, y + 3)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.set_text_color(*MUTED)
        pdf.cell(card_width - 6, 4, label.upper(), ln=True)

        pdf.set_x(x + 3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(*color)
        pdf.cell(card_width - 6, 8, clean_text(value), ln=True)

    pdf.set_y(y + card_height + 6)


def add_clean_table(
    pdf: FPDF,
    rows: list[tuple[str, str]],
    col1: str = "Metric",
    col2: str = "Value",
) -> None:
    table_width = pdf.w - pdf.l_margin - pdf.r_margin
    col1_width = table_width * 0.58
    col2_width = table_width * 0.42
    row_height = 8

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(*PRIMARY)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(col1_width, row_height, col1, border=0, fill=True)
    pdf.cell(col2_width, row_height, col2, border=0, fill=True, ln=True)

    pdf.set_font("Helvetica", "", 9)

    for i, (metric, value) in enumerate(rows):
        if i % 2 == 0:
            pdf.set_fill_color(250, 251, 252)
        else:
            pdf.set_fill_color(255, 255, 255)

        pdf.set_text_color(40, 45, 52)
        pdf.cell(col1_width, row_height, clean_text(metric), border="B", fill=True)

        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(col2_width, row_height, clean_text(value), border="B", fill=True, ln=True)

        pdf.set_font("Helvetica", "", 9)

    pdf.ln(5)


def add_stock_metrics_table(pdf: FPDF, metrics: dict) -> None:
    rows = [
        ("Latest Closing Price", f"${metrics['latest_close']}"),
        ("7-Day Return", f"{metrics['seven_day_return']}%"),
        ("30-Day Return", f"{metrics['thirty_day_return']}%"),
        ("Daily Volatility", f"{metrics['daily_volatility']}%"),
        ("20-Day Moving Average", f"{metrics['ma20']}"),
        ("50-Day Moving Average", f"{metrics['ma50']}"),
        ("Highest Closing Price in Period", f"${metrics['highest_price']}"),
        ("Lowest Closing Price in Period", f"${metrics['lowest_price']}"),
    ]

    add_clean_table(pdf, rows)


def add_financials_table(pdf: FPDF, financials: dict) -> None:
    rows = [
        ("Total Revenue", financials["total_revenue"]),
        ("Net Income", financials["net_income"]),
        ("Total Assets", financials["total_assets"]),
        ("Total Liabilities", financials["total_liabilities"]),
        ("Operating Cash Flow", financials["operating_cash_flow"]),
        ("Free Cash Flow", financials["free_cash_flow"]),
        ("Profit Margin", financials["profit_margin"]),
        ("Debt-to-Assets Ratio", financials["debt_to_assets"]),
    ]

    add_clean_table(pdf, rows)


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
                "The 20-day and 50-day moving averages are close, suggesting a neutral trend."
            )

    return " ".join(summary)


def add_chart(pdf: FPDF, title: str, chart_path: str) -> None:
    add_section_title(pdf, title)

    if os.path.exists(chart_path):
        available_width = pdf.w - pdf.l_margin - pdf.r_margin
        pdf.image(chart_path, x=pdf.l_margin + 4, w=available_width - 8)
        pdf.ln(5)
    else:
        add_paragraph(pdf, f"Chart not found: {chart_path}")


def generate_pdf_report(
    ticker: str,
    company_info: dict,
    metrics: dict,
    price_chart_path: str,
    moving_average_chart_path: str,
    financials: dict | None = None,
    financials_summary: str | None = None,
    ai_analysis: str | None = None,
) -> str:
    os.makedirs("reports/pdf", exist_ok=True)
    pdf_path = f"reports/pdf/{ticker}_report.pdf"

    pdf = FinancialReportPDF()
    pdf.report_title = f"{company_info.get('company_name', ticker)} ({ticker})"
    pdf.add_page()

    add_title_page_header(pdf, company_info, ticker)

    add_section_title(pdf, "1. Company Snapshot")
    add_info_grid(pdf, company_info)

    add_subsection_title(pdf, "Business Summary")
    add_paragraph(
        pdf,
        company_info.get("business_summary", "No summary available."),
        font_size=9,
        line_height=5.3,
    )

    add_section_title(pdf, "2. Key Market Metrics")
    add_metric_cards(pdf, metrics)
    add_stock_metrics_table(pdf, metrics)

    pdf.add_page()
    add_chart(pdf, "3. Price Chart", price_chart_path)
    add_chart(pdf, "4. Moving Average Chart", moving_average_chart_path)

    add_section_title(pdf, "5. Automated Financial Summary")
    add_paragraph(pdf, generate_rule_based_summary(metrics))

    if financials is not None:
        add_section_title(pdf, "6. Company Financial Highlights")
        add_financials_table(pdf, financials)

        add_subsection_title(pdf, "Financial Statement Summary")

        if financials_summary is None:
            financials_summary = "No financial statement summary available."

        add_paragraph(pdf, financials_summary)

    if ai_analysis is not None:
        pdf.add_page()
        add_section_title(pdf, "7. Local Llama AI-Generated Financial Analysis")

        for heading, body in parse_ai_sections(ai_analysis):
            add_subsection_title(pdf, heading)
            add_paragraph(pdf, body)

    add_section_title(pdf, "8. Disclaimer")

    disclaimer = (
        "This report is generated automatically using public market data and local AI text generation. "
        "It is for educational and informational purposes only and should not be considered financial advice."
    )

    add_paragraph(pdf, disclaimer, font_size=9, line_height=5.3)

    pdf.output(pdf_path)

    return pdf_path