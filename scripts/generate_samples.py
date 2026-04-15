#!/usr/bin/env python3
"""
Generate synthetic sample documents for testing the OCR tab.
Creates:
  - sample_invoice.png       (image of a professional invoice)
  - sample_workorder.png     (image of a work order)
  - sample_receipt.png       (image of a receipt)
  - sample_invoice.pdf       (PDF invoice)
  - sample_purchase_order.pdf(PDF purchase order)
  - sample_accounts_payable.csv (additional sample data)
"""

import os
import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

OUTPUT_DIR = PROJECT_ROOT / "sample_data"
OUTPUT_DIR.mkdir(exist_ok=True)

from PIL import Image, ImageDraw, ImageFont


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _get_font(size: int = 16):
    """Try to load a monospaced font, fall back to default."""
    candidates = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Courier.dfont",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _get_bold_font(size: int = 18):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return _get_font(size)


def _draw_text_block(draw, lines, x, y, font, spacing=4, color="black"):
    """Draw multiple lines of text."""
    for line in lines:
        draw.text((x, y), line, fill=color, font=font)
        y += font.size + spacing
    return y


# ---------------------------------------------------------------------------
# 1) Invoice Image
# ---------------------------------------------------------------------------
def create_invoice_image():
    W, H = 800, 1100
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    font = _get_font(15)
    bold = _get_bold_font(20)
    small = _get_font(12)

    # Header
    draw.rectangle([(0, 0), (W, 80)], fill="#1a365d")
    draw.text((30, 20), "ACME CONSULTING GROUP", fill="white", font=_get_bold_font(26))
    draw.text((30, 52), "123 Business Ave, Suite 400, San Francisco, CA 94102", fill="#cbd5e0", font=small)

    # Invoice title
    draw.text((580, 100), "INVOICE", fill="#1a365d", font=_get_bold_font(30))

    y = 140
    lines = [
        "Invoice No:    INV-2026-0847",
        "Date:          March 15, 2026",
        "Due Date:      April 14, 2026",
        "Terms:         Net 30",
    ]
    _draw_text_block(draw, lines, 500, y, font, spacing=6)

    # Bill To
    y = 140
    draw.text((40, y), "BILL TO:", fill="#4a5568", font=_get_bold_font(14))
    y += 24
    bill_to = [
        "TechForward Inc.",
        "Attn: Accounts Payable",
        "456 Innovation Blvd",
        "Austin, TX 78701",
        "EIN: 84-2937561",
    ]
    _draw_text_block(draw, bill_to, 40, y, font, spacing=4)

    # Line items table
    y = 330
    draw.line([(30, y), (770, y)], fill="#1a365d", width=2)
    y += 5
    headers = f"{'Description':<35} {'Qty':>5} {'Unit Price':>12} {'Amount':>12}"
    draw.text((40, y), headers, fill="#1a365d", font=_get_bold_font(14))
    y += 28
    draw.line([(30, y), (770, y)], fill="#e2e8f0", width=1)
    y += 8

    items = [
        ("Financial Systems Audit (Q1)",    1,  18500.00),
        ("Tax Compliance Review",           1,  12000.00),
        ("Monthly Bookkeeping - Jan 2026",  1,   4500.00),
        ("Monthly Bookkeeping - Feb 2026",  1,   4500.00),
        ("Monthly Bookkeeping - Mar 2026",  1,   4500.00),
        ("Custom Financial Dashboard Dev",  40,   250.00),
        ("Staff Training (2 sessions)",     2,   3000.00),
    ]

    subtotal = 0
    for desc, qty, unit in items:
        amt = qty * unit
        subtotal += amt
        line = f"{desc:<35} {qty:>5} ${unit:>10,.2f} ${amt:>10,.2f}"
        draw.text((40, y), line, fill="black", font=font)
        y += 24

    y += 8
    draw.line([(30, y), (770, y)], fill="#1a365d", width=2)
    y += 12

    # Totals
    tax_rate = 0.0875
    tax = round(subtotal * tax_rate, 2)
    total = subtotal + tax

    totals = [
        f"{'Subtotal:':>55} ${subtotal:>10,.2f}",
        f"{'Sales Tax (8.75%):':>55} ${tax:>10,.2f}",
    ]
    _draw_text_block(draw, totals, 40, y, font, spacing=6)
    y += 50
    draw.line([(450, y), (770, y)], fill="#1a365d", width=2)
    y += 8
    draw.text((40, y), f"{'TOTAL DUE:':>55} ${total:>10,.2f}", fill="#1a365d", font=_get_bold_font(16))

    # Payment info
    y += 60
    draw.line([(30, y), (770, y)], fill="#e2e8f0", width=1)
    y += 12
    draw.text((40, y), "PAYMENT INFORMATION", fill="#1a365d", font=_get_bold_font(14))
    y += 24
    pay_lines = [
        "Bank:         First National Bank",
        "Account:      ACME Consulting Group",
        "Routing No:   021000021",
        "Account No:   4829-3371-0056",
        "Reference:    INV-2026-0847",
    ]
    _draw_text_block(draw, pay_lines, 40, y, font, spacing=4)

    # Footer
    y = H - 60
    draw.line([(30, y), (770, y)], fill="#e2e8f0", width=1)
    draw.text((40, y + 10), "Thank you for your business!", fill="#4a5568", font=small)
    draw.text((40, y + 28), "Questions? accounts@acmeconsulting.com | (415) 555-0198", fill="#a0aec0", font=small)

    path = OUTPUT_DIR / "sample_invoice.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")
    return path


# ---------------------------------------------------------------------------
# 2) Work Order Image
# ---------------------------------------------------------------------------
def create_workorder_image():
    W, H = 800, 950
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    font = _get_font(15)
    bold = _get_bold_font(18)
    small = _get_font(12)

    # Header
    draw.rectangle([(0, 0), (W, 70)], fill="#065f46")
    draw.text((30, 18), "GREENFIELD FACILITIES MANAGEMENT", fill="white", font=_get_bold_font(22))
    draw.text((30, 48), "Work Order Authorization", fill="#a7f3d0", font=small)

    y = 90
    draw.text((560, y), "WORK ORDER", fill="#065f46", font=_get_bold_font(24))

    # WO details
    y = 130
    details = [
        "WO Number:     WO-2026-1134",
        "Date Issued:   March 28, 2026",
        "Priority:      HIGH",
        "Status:        APPROVED",
    ]
    _draw_text_block(draw, details, 450, y, font, spacing=5)

    y = 130
    draw.text((40, y), "REQUESTED BY:", fill="#4a5568", font=_get_bold_font(13))
    y += 22
    req = [
        "Sarah Chen, Operations Director",
        "TechForward Inc.",
        "456 Innovation Blvd, Floor 3",
        "Austin, TX 78701",
    ]
    _draw_text_block(draw, req, 40, y, font, spacing=3)

    y += 80
    draw.text((40, y), "ASSIGNED TO:", fill="#4a5568", font=_get_bold_font(13))
    y += 22
    assigned = [
        "ProBuild Contractors LLC",
        "Contact: Mike Torres",
        "Phone: (512) 555-0342",
        "License: TX-CON-88451",
    ]
    _draw_text_block(draw, assigned, 40, y, font, spacing=3)

    # Description
    y = 380
    draw.line([(30, y), (770, y)], fill="#065f46", width=2)
    y += 10
    draw.text((40, y), "DESCRIPTION OF WORK", fill="#065f46", font=bold)
    y += 28
    desc = [
        "Emergency HVAC repair for server room cooling system (Unit AC-07).",
        "Compressor failure detected on March 27. Server room temperature rising",
        "above acceptable threshold (78 F). Immediate repair required to prevent",
        "equipment damage. Includes diagnostic, compressor replacement, refrigerant",
        "recharge, and full system test.",
    ]
    _draw_text_block(draw, desc, 40, y, font, spacing=4)

    y += 110
    draw.text((40, y), "LOCATION: Building A, Server Room 3-East", fill="black", font=font)

    # Materials table
    y += 40
    draw.line([(30, y), (770, y)], fill="#065f46", width=2)
    y += 8
    draw.text((40, y), "MATERIALS & LABOR ESTIMATE", fill="#065f46", font=bold)
    y += 28
    draw.text((40, y), f"{'Item':<35} {'Qty':>5} {'Unit Cost':>12} {'Total':>12}", fill="#065f46", font=_get_bold_font(13))
    y += 22
    draw.line([(30, y), (770, y)], fill="#e2e8f0", width=1)
    y += 6

    materials = [
        ("Scroll Compressor ZR48K3-TF5",   1, 2850.00),
        ("R-410A Refrigerant (25 lb)",      2,  385.00),
        ("Contactor 40A 24V coil",          1,   85.00),
        ("Copper tubing & fittings",        1,  220.00),
        ("Diagnostic & Labor (hours)",      8,  175.00),
        ("Emergency surcharge",             1,  500.00),
    ]

    total = 0
    for desc, qty, unit in materials:
        amt = qty * unit
        total += amt
        line = f"{desc:<35} {qty:>5} ${unit:>10,.2f} ${amt:>10,.2f}"
        draw.text((40, y), line, fill="black", font=font)
        y += 22

    y += 8
    draw.line([(30, y), (770, y)], fill="#065f46", width=2)
    y += 10
    draw.text((40, y), f"{'ESTIMATED TOTAL:':>55} ${total:>10,.2f}", fill="#065f46", font=bold)

    # Approval
    y += 50
    draw.text((40, y), "Approved By:  James Wright, VP Facilities", fill="black", font=font)
    y += 22
    draw.text((40, y), "Date Approved: March 28, 2026", fill="black", font=font)
    y += 22
    draw.text((40, y), "Target Completion: March 30, 2026", fill="black", font=font)

    path = OUTPUT_DIR / "sample_workorder.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")
    return path


# ---------------------------------------------------------------------------
# 3) Receipt Image
# ---------------------------------------------------------------------------
def create_receipt_image():
    W, H = 420, 700
    img = Image.new("RGB", (W, H), "#fefef9")
    draw = ImageDraw.Draw(img)
    font = _get_font(14)
    bold = _get_bold_font(16)
    small = _get_font(11)

    y = 20
    draw.text((W // 2 - 100, y), "OFFICE DEPOT", fill="black", font=_get_bold_font(24))
    y += 35
    center_lines = [
        "Store #4521",
        "789 Commerce St, Austin TX 78701",
        "Tel: (512) 555-0211",
    ]
    for line in center_lines:
        tw = len(line) * 7
        draw.text((W // 2 - tw // 2, y), line, fill="#555", font=small)
        y += 16

    y += 10
    draw.line([(20, y), (W - 20, y)], fill="#999", width=1)
    y += 8

    info = [
        "Date: 03/10/2026  Time: 14:32",
        "Cashier: T. Martinez",
        "Trans #: 452100873",
    ]
    _draw_text_block(draw, info, 30, y, small, spacing=3)
    y += 55

    draw.line([(20, y), (W - 20, y)], fill="#999", width=1)
    y += 8

    items = [
        ("HP 64XL Ink Black",        2,  38.99),
        ("HP 64XL Ink Color",        1,  42.99),
        ("Copy Paper 10-ream",       2,  54.99),
        ("Stapler Heavy Duty",       1,  24.99),
        ("Binder Clips Asst 60pk",   3,   6.49),
        ("Legal Pads Yellow 12pk",   1,  15.99),
        ("USB-C Cable 6ft",          2,  12.99),
    ]

    subtotal = 0
    for desc, qty, price in items:
        amt = qty * price
        subtotal += amt
        draw.text((30, y), f"{desc}", fill="black", font=font)
        y += 18
        draw.text((50, y), f"{qty} x ${price:.2f}", fill="#666", font=small)
        draw.text((W - 90, y), f"${amt:.2f}", fill="black", font=font)
        y += 22

    y += 5
    draw.line([(20, y), (W - 20, y)], fill="#999", width=1)
    y += 10

    tax = round(subtotal * 0.0825, 2)
    total = subtotal + tax

    draw.text((30, y), "Subtotal:", fill="black", font=font)
    draw.text((W - 90, y), f"${subtotal:.2f}", fill="black", font=font)
    y += 22
    draw.text((30, y), "Tax (8.25%):", fill="black", font=font)
    draw.text((W - 90, y), f"${tax:.2f}", fill="black", font=font)
    y += 26
    draw.line([(20, y), (W - 20, y)], fill="black", width=2)
    y += 8
    draw.text((30, y), "TOTAL:", fill="black", font=bold)
    draw.text((W - 100, y), f"${total:.2f}", fill="black", font=bold)
    y += 30

    draw.text((30, y), "Payment: VISA ****4821", fill="black", font=font)
    y += 20
    draw.text((30, y), f"Amount Charged: ${total:.2f}", fill="black", font=font)
    y += 20
    draw.text((30, y), "Auth Code: 884523", fill="#666", font=small)

    y += 35
    draw.line([(20, y), (W - 20, y)], fill="#999", width=1)
    y += 10
    for line in ["Returns within 30 days with receipt", "Thank you for shopping with us!"]:
        tw = len(line) * 6
        draw.text((W // 2 - tw // 2, y), line, fill="#888", font=small)
        y += 16

    path = OUTPUT_DIR / "sample_receipt.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")
    return path


# ---------------------------------------------------------------------------
# 4 & 5) PDF documents (using simple image-based approach for portability)
# ---------------------------------------------------------------------------
def create_invoice_pdf():
    """Create a PDF invoice by rendering to image first, then saving as PDF."""
    W, H = 800, 1100
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    font = _get_font(14)
    bold = _get_bold_font(18)
    small = _get_font(11)

    draw.rectangle([(0, 0), (W, 70)], fill="#7c3aed")
    draw.text((30, 18), "SUMMIT FINANCIAL SERVICES", fill="white", font=_get_bold_font(24))
    draw.text((30, 48), "789 Wall Street, New York, NY 10005 | (212) 555-0399", fill="#ddd6fe", font=small)

    draw.text((560, 90), "INVOICE", fill="#7c3aed", font=_get_bold_font(28))

    y = 130
    inv_details = [
        "Invoice #:  SFS-2026-2241",
        "Date:       April 01, 2026",
        "Due Date:   May 01, 2026",
        "PO Ref:     PO-TF-9982",
    ]
    _draw_text_block(draw, inv_details, 480, y, font, spacing=5)

    y = 130
    draw.text((40, y), "BILL TO:", fill="#6b7280", font=_get_bold_font(12))
    y += 20
    bt = [
        "GlobalTech Manufacturing",
        "Accounts Payable Department",
        "1200 Industrial Parkway",
        "Detroit, MI 48201",
        "Tax ID: 38-4829174",
    ]
    _draw_text_block(draw, bt, 40, y, font, spacing=3)

    y = 310
    draw.line([(30, y), (770, y)], fill="#7c3aed", width=2)
    y += 8
    draw.text((40, y), f"{'Service Description':<32} {'Period':>14} {'Hours':>7} {'Rate':>10} {'Amount':>12}",
              fill="#7c3aed", font=_get_bold_font(12))
    y += 22
    draw.line([(30, y), (770, y)], fill="#e5e7eb")
    y += 6

    services = [
        ("Annual Financial Audit",      "Q1 2026",    120, 275.00),
        ("Tax Preparation (Federal)",   "FY 2025",     40, 300.00),
        ("Tax Preparation (State-MI)",  "FY 2025",     16, 300.00),
        ("Forensic Accounting Review",  "Feb 2026",    32, 350.00),
        ("Payroll Processing",          "Jan-Mar 26",  60, 125.00),
        ("CFO Advisory Services",       "Q1 2026",     24, 450.00),
    ]

    subtotal = 0
    for desc, period, hrs, rate in services:
        amt = hrs * rate
        subtotal += amt
        line = f"{desc:<32} {period:>14} {hrs:>7} ${rate:>8,.2f} ${amt:>10,.2f}"
        draw.text((40, y), line, fill="black", font=font)
        y += 22

    y += 10
    draw.line([(30, y), (770, y)], fill="#7c3aed", width=2)
    y += 10

    tax = round(subtotal * 0.08875, 2)
    total = subtotal + tax

    draw.text((400, y), f"Subtotal:           ${subtotal:>12,.2f}", fill="black", font=font)
    y += 22
    draw.text((400, y), f"NY Sales Tax (8.875%): ${tax:>10,.2f}", fill="black", font=font)
    y += 28
    draw.line([(450, y), (770, y)], fill="#7c3aed", width=2)
    y += 8
    draw.text((400, y), f"AMOUNT DUE:         ${total:>12,.2f}", fill="#7c3aed", font=bold)

    y += 60
    draw.line([(30, y), (770, y)], fill="#e5e7eb")
    y += 10
    draw.text((40, y), "PAYMENT INSTRUCTIONS", fill="#7c3aed", font=_get_bold_font(13))
    y += 22
    pay = [
        "Wire Transfer: JPMorgan Chase  |  Routing: 021000021  |  Acct: 9928-4411-7753",
        "Reference: SFS-2026-2241",
        "Late payments subject to 1.5% monthly interest after due date.",
    ]
    _draw_text_block(draw, pay, 40, y, small, spacing=4)

    path = OUTPUT_DIR / "sample_invoice.pdf"
    img.save(path, "PDF", resolution=150)
    print(f"  Created: {path}")


def create_purchase_order_pdf():
    W, H = 800, 1000
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    font = _get_font(14)
    bold = _get_bold_font(18)
    small = _get_font(11)

    draw.rectangle([(0, 0), (W, 70)], fill="#b45309")
    draw.text((30, 18), "GLOBALTECH MANUFACTURING", fill="white", font=_get_bold_font(22))
    draw.text((30, 48), "1200 Industrial Parkway, Detroit, MI 48201", fill="#fde68a", font=small)

    draw.text((520, 90), "PURCHASE ORDER", fill="#b45309", font=_get_bold_font(22))

    y = 130
    po_info = [
        "PO Number:     PO-GT-2026-0553",
        "Date:          April 05, 2026",
        "Delivery By:   April 20, 2026",
        "Payment Terms: Net 45",
    ]
    _draw_text_block(draw, po_info, 440, y, font, spacing=5)

    y = 130
    draw.text((40, y), "VENDOR:", fill="#6b7280", font=_get_bold_font(12))
    y += 20
    vendor = [
        "Precision Parts Supply Co.",
        "8900 Manufacturing Row",
        "Cleveland, OH 44101",
        "Contact: Angela Reed",
        "Phone: (216) 555-0478",
    ]
    _draw_text_block(draw, vendor, 40, y, font, spacing=3)

    y += 90
    draw.text((40, y), "SHIP TO:", fill="#6b7280", font=_get_bold_font(12))
    y += 20
    ship = [
        "GlobalTech Mfg - Receiving Dock B",
        "1200 Industrial Parkway",
        "Detroit, MI 48201",
    ]
    _draw_text_block(draw, ship, 40, y, font, spacing=3)

    y = 400
    draw.line([(30, y), (770, y)], fill="#b45309", width=2)
    y += 8
    draw.text((40, y), f"{'Part / Description':<30} {'Part No.':>12} {'Qty':>6} {'Unit Price':>12} {'Total':>12}",
              fill="#b45309", font=_get_bold_font(12))
    y += 22
    draw.line([(30, y), (770, y)], fill="#e5e7eb")
    y += 6

    items = [
        ("CNC Bearing Assembly",     "PPS-BA-4420",  50,  124.50),
        ("Stainless Steel Rod 12mm", "PPS-SR-1200", 200,   18.75),
        ("Hydraulic Seal Kit",       "PPS-HS-8800",  30,   67.90),
        ("Titanium Bolt Set M8",     "PPS-TB-0800", 500,    4.25),
        ("Precision Gear Set",       "PPS-PG-3300",  20,  289.00),
        ("Coolant Fluid 5-gal",      "PPS-CF-5000",  10,   85.00),
    ]

    subtotal = 0
    for desc, part, qty, unit in items:
        amt = qty * unit
        subtotal += amt
        line = f"{desc:<30} {part:>12} {qty:>6} ${unit:>10,.2f} ${amt:>10,.2f}"
        draw.text((40, y), line, fill="black", font=font)
        y += 22

    y += 10
    draw.line([(30, y), (770, y)], fill="#b45309", width=2)
    y += 10

    shipping = 850.00
    tax = round(subtotal * 0.06, 2)
    total = subtotal + shipping + tax

    draw.text((400, y), f"Subtotal:          ${subtotal:>12,.2f}", fill="black", font=font); y += 22
    draw.text((400, y), f"Shipping:          ${shipping:>12,.2f}", fill="black", font=font); y += 22
    draw.text((400, y), f"MI Sales Tax (6%): ${tax:>12,.2f}", fill="black", font=font); y += 26
    draw.line([(450, y), (770, y)], fill="#b45309", width=2); y += 8
    draw.text((400, y), f"GRAND TOTAL:       ${total:>12,.2f}", fill="#b45309", font=bold)

    y += 50
    draw.line([(30, y), (770, y)], fill="#e5e7eb"); y += 10
    draw.text((40, y), "Authorized By: Patricia Lane, Procurement Director", fill="black", font=font)
    y += 22
    draw.text((40, y), "Date: April 05, 2026", fill="black", font=font)
    y += 30
    draw.text((40, y), "Special Instructions: Deliver to Dock B, notify receiving 24h in advance.",
              fill="#6b7280", font=small)

    path = OUTPUT_DIR / "sample_purchase_order.pdf"
    img.save(path, "PDF", resolution=150)
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# Additional sample CSV
# ---------------------------------------------------------------------------
def create_accounts_payable_csv():
    import csv
    rows = [
        ["Vendor", "Invoice No", "Invoice Date", "Due Date", "Amount", "Status", "Category"],
        ["Precision Parts Supply", "PPS-INV-4521", "2026-01-15", "2026-03-01", "28750.00", "Paid", "Materials"],
        ["ProBuild Contractors", "PBC-2026-088", "2026-01-22", "2026-02-21", "15400.00", "Paid", "Maintenance"],
        ["Office Depot", "OD-78432", "2026-02-03", "2026-03-05", "2847.50", "Paid", "Office Supplies"],
        ["Acme Consulting Group", "INV-2026-0847", "2026-03-15", "2026-04-14", "58906.25", "Outstanding", "Professional Services"],
        ["Summit Financial", "SFS-2026-2241", "2026-04-01", "2026-05-01", "105827.19", "Outstanding", "Professional Services"],
        ["CloudHost Inc.", "CH-26-0091", "2026-02-01", "2026-03-03", "4200.00", "Paid", "IT Services"],
        ["CloudHost Inc.", "CH-26-0182", "2026-03-01", "2026-04-01", "4200.00", "Overdue", "IT Services"],
        ["Delta Insurance", "DI-POL-8843", "2026-01-10", "2026-02-10", "12600.00", "Paid", "Insurance"],
        ["EcoClean Services", "EC-2026-334", "2026-03-01", "2026-03-31", "3200.00", "Paid", "Facilities"],
        ["EcoClean Services", "EC-2026-445", "2026-04-01", "2026-04-30", "3200.00", "Outstanding", "Facilities"],
        ["TechParts Direct", "TPD-99281", "2026-02-18", "2026-04-04", "19825.00", "Overdue", "Materials"],
        ["Greenfield Facilities", "GF-WO-1134", "2026-03-28", "2026-04-28", "6325.00", "Outstanding", "Maintenance"],
    ]
    path = OUTPUT_DIR / "sample_accounts_payable.csv"
    with open(path, "w", newline="") as f:
        csv.writer(f).writerows(rows)
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating synthetic sample documents …")
    create_invoice_image()
    create_workorder_image()
    create_receipt_image()
    create_invoice_pdf()
    create_purchase_order_pdf()
    create_accounts_payable_csv()
    print("Done!")
