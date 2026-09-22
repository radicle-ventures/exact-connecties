import sys
from datetime import datetime

from fpdf import FPDF

import auth
import exact_api


def format_eur(amount):
    """Format a number as EUR with thousands separator."""
    return f"EUR {amount:,.2f}"


def generate_pdf(data, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Calculate grand total upfront
    grand_total = sum(
        sum(b["balance"] for b in entity["balances"])
        for entity in data
    )

    # Title
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 12, "Bank Balances - Exact Online", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 6, datetime.now().strftime("%d %B %Y, %H:%M"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    # Grand total at the top
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(60, 10, "Total All Entities:")
    pdf.cell(105, 10, format_eur(grand_total), align="R")
    pdf.ln(14)

    for entity in data:
        name = entity["name"]
        code = entity["code"]
        balances = entity["balances"]

        # Entity header
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 8, f"  {name} ({code})", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.ln(2)

        if not balances:
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, "  No bank accounts found.", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)
            continue

        # Table header
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(20, 6, "Code", border="B")
        pdf.cell(70, 6, "Description", border="B")
        pdf.cell(40, 6, "Balance", border="B", align="R")
        pdf.cell(35, 6, "Last Transaction", border="B", align="R")
        pdf.ln()

        # Rows
        pdf.set_font("Helvetica", "", 9)
        entity_total = 0.0
        for b in balances:
            last_tx = b.get("last_transaction")
            last_tx_str = last_tx.strftime("%d-%m-%Y") if last_tx else "-"
            pdf.cell(20, 6, b["code"])
            pdf.cell(70, 6, b["name"])
            pdf.cell(40, 6, format_eur(b["balance"]), align="R")
            pdf.cell(35, 6, last_tx_str, align="R")
            pdf.ln()
            entity_total += b["balance"]

        # Entity subtotal
        pdf.set_font("Helvetica", "B", 9)
        pdf.cell(90, 6, "Subtotal", border="T")
        pdf.cell(40, 6, format_eur(entity_total), border="T", align="R")
        pdf.cell(35, 6, "", border="T")
        pdf.ln(10)


    pdf.output(filename)
    return filename


def main():
    try:
        token = auth.get_valid_token()
    except Exception as e:
        print(f"Authentication failed: {e}")
        sys.exit(1)

    print("\nFetching divisions...")
    divisions = exact_api.get_divisions(token)

    if not divisions:
        print("No divisions found.")
        sys.exit(0)

    data = []
    for div in divisions:
        code = div.get("Code")
        name = div.get("Description", "Unknown")
        print(f"  Fetching balances for {name}...")
        balances = exact_api.get_bank_balances(token, code)
        data.append({"name": name, "code": code, "balances": balances})

    filename = f"bank_balances_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    generate_pdf(data, filename)
    print(f"\nPDF saved: {filename}")


if __name__ == "__main__":
    main()
