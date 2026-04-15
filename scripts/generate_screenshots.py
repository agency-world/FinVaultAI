#!/usr/bin/env python3
"""
Generate polished screenshots for documentation and marketing materials.
Creates realistic composite screenshots of each major app screen.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

OUTPUT_DIR = PROJECT_ROOT / "docs" / "screenshots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Font helpers
# ---------------------------------------------------------------------------
def _font(size=16):
    for p in ["/System/Library/Fonts/SFNSMono.ttf",
              "/System/Library/Fonts/Menlo.ttc",
              "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

def _bold(size=18):
    for p in ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return _font(size)

# ---------------------------------------------------------------------------
# Color palette (matches dark theme)
# ---------------------------------------------------------------------------
BG = "#0f1117"
CARD_BG = "#1a1c2e"
BORDER = "#334155"
INDIGO = "#6366f1"
INDIGO_LIGHT = "#a5b4fc"
INDIGO_DIM = "#1e1b4b"
GREEN = "#22c55e"
GREEN_DIM = "#22c55e30"
TEXT = "#e2e8f0"
TEXT_DIM = "#94a3b8"
TEXT_MUTED = "#64748b"
WHITE = "#ffffff"
AMBER = "#fbbf24"

def hex_to_rgb(h):
    h = h.lstrip("#")
    if len(h) == 8:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4, 6))
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


# ---------------------------------------------------------------------------
# 1) Dashboard / Landing screenshot
# ---------------------------------------------------------------------------
def create_dashboard_screenshot():
    W, H = 1440, 900
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f14 = _font(14); f12 = _font(12); f10 = _font(10)
    b24 = _bold(24); b18 = _bold(18); b14 = _bold(14); b12 = _bold(12)

    # Sidebar background
    draw.rectangle([(0, 0), (200, H)], fill=CARD_BG)
    draw.line([(200, 0), (200, H)], fill=BORDER, width=1)

    # Sidebar branding
    draw.text((55, 30), "FinVault AI", fill=INDIGO_LIGHT, font=b18)
    draw.text((42, 55), "PRIVATE BY DESIGN", fill=TEXT_MUTED, font=_font(9))

    # Security badge
    draw.rounded_rectangle([(18, 80), (182, 100)], radius=12, fill="#22c55e15", outline=GREEN_DIM)
    draw.text((24, 84), "OFFLINE  *  AIR-GAPPED  *  SECURE", fill=GREEN, font=_font(8))

    # Connection section
    draw.text((16, 125), "CONNECTION", fill=TEXT_DIM, font=_font(9))
    draw.rounded_rectangle([(12, 145), (188, 168)], radius=6, fill="#0f1117", outline=BORDER)
    draw.text((18, 150), "http://localhost:1234/v1", fill=TEXT_DIM, font=f10)

    draw.rounded_rectangle([(12, 178), (188, 198)], radius=6, fill="#0f1117", outline=BORDER)
    draw.text((18, 183), "google/gemma-4-e4b", fill=TEXT, font=f10)

    # Connected indicator
    draw.rounded_rectangle([(12, 210), (188, 245)], radius=8, fill="#22c55e10", outline=GREEN_DIM)
    draw.ellipse([(20, 222), (28, 230)], fill=GREEN)
    draw.text((34, 218), "Connected", fill=GREEN, font=b12)
    draw.text((20, 234), "google/gemma-4-e4b", fill=TEXT_DIM, font=_font(8))

    # Admin
    draw.text((16, 265), "ADMIN", fill=TEXT_DIM, font=_font(9))
    draw.rounded_rectangle([(12, 285), (188, 310)], radius=6, fill=CARD_BG, outline=BORDER)
    draw.text((18, 291), "Model & Inference", fill=TEXT, font=b12)

    # Model card
    draw.rounded_rectangle([(16, 320), (184, 370)], radius=6, fill=INDIGO_DIM, outline="#6366f130")
    draw.text((22, 325), "ACTIVE MODEL", fill=INDIGO, font=_font(8))
    draw.text((22, 338), "Gemma 4", fill=TEXT, font=b14)
    draw.text((22, 356), "google/gemma-4-e4b", fill=TEXT_DIM, font=_font(8))

    # Sliders
    labels = [("Temperature", "0.15", 385), ("Max Tokens", "2048", 420), ("Top-P", "0.95", 455)]
    for label, val, y in labels:
        draw.text((16, y), label, fill=TEXT_DIM, font=f10)
        draw.text((155, y), val, fill=INDIGO_LIGHT, font=f10)
        draw.rounded_rectangle([(16, y+15), (184, y+19)], radius=2, fill=BORDER)
        draw.rounded_rectangle([(16, y+15), (60, y+19)], radius=2, fill=INDIGO)

    # System Health
    draw.rounded_rectangle([(12, 490), (188, 515)], radius=6, fill=CARD_BG, outline=BORDER)
    draw.text((18, 496), "System Health", fill=TEXT, font=b12)

    # About
    draw.rounded_rectangle([(12, 525), (188, 550)], radius=6, fill=CARD_BG, outline=BORDER)
    draw.text((18, 531), "About", fill=TEXT, font=b12)

    # ===== MAIN CONTENT =====
    # Header card
    draw.rounded_rectangle([(220, 20), (1420, 120)], radius=16, fill=INDIGO_DIM, outline="#6366f125")
    # Gradient glow (simulated)
    for i in range(30):
        alpha = max(0, 15 - i)
        draw.ellipse([(1100-i*5, 20-i*2), (1420+i*2, 120+i*2)], fill=None, outline=f"#{alpha:02x}{alpha:02x}{50+alpha:02x}")
    draw.text((250, 35), "FinVault AI", fill=INDIGO_LIGHT, font=_bold(30))
    draw.text((250, 72), "On-device financial intelligence. Private by design.", fill=TEXT_DIM, font=f14)
    # Badges
    badges = [("Air-Gapped", GREEN, 250), ("Gemma 4 Powered", INDIGO_LIGHT, 360), ("Zero Cloud", AMBER, 510)]
    for text, color, x in badges:
        draw.rounded_rectangle([(x, 95), (x+100, 113)], radius=10, fill=f"{color}15", outline=f"{color}35")
        draw.text((x+8, 99), text, fill=color, font=_font(9))

    # Tabs
    tab_y = 140
    draw.rounded_rectangle([(220, tab_y), (620, tab_y+40)], radius=10, fill=CARD_BG, outline=BORDER)
    # Active tab
    draw.rounded_rectangle([(224, tab_y+4), (354, tab_y+36)], radius=8, fill=INDIGO)
    draw.text((244, tab_y+12), "Report Generator", fill=WHITE, font=b12)
    draw.text((374, tab_y+12), "Data Query", fill=TEXT_DIM, font=b12)
    draw.text((484, tab_y+12), "Document OCR", fill=TEXT_DIM, font=b12)

    # Content area
    draw.text((230, 200), "Upload accounting data and generate professional internal reports", fill=TEXT_DIM, font=f12)

    # Data table
    draw.rounded_rectangle([(230, 230), (1410, 440)], radius=10, fill=CARD_BG, outline=BORDER)
    draw.text((245, 240), "Data Preview (20 rows x 7 columns)", fill=TEXT, font=b12)

    # Table headers
    headers = ["Date", "Account", "Category", "Description", "Debit", "Credit", "Balance"]
    hx = [260, 380, 470, 590, 780, 900, 1020]
    for i, (h, x) in enumerate(zip(headers, hx)):
        draw.text((x, 270), h, fill=INDIGO_LIGHT, font=b12)
    draw.line([(245, 288), (1395, 288)], fill=BORDER)

    rows = [
        ("2026-01-05", "1001", "Revenue", "Product Sales Q1", "0", "125,000", "125,000"),
        ("2026-01-10", "2001", "COGS", "Raw Materials Purchase", "45,000", "0", "80,000"),
        ("2026-01-15", "3001", "Operating Expense", "Office Rent - January", "8,500", "0", "71,500"),
        ("2026-01-20", "3002", "Operating Expense", "Employee Salaries - Jan", "52,000", "0", "19,500"),
        ("2026-02-05", "1001", "Revenue", "Product Sales Feb", "0", "98,000", "115,300"),
    ]
    for ri, row in enumerate(rows):
        y = 296 + ri * 26
        bg = "#0f111720" if ri % 2 == 0 else CARD_BG
        for ci, (val, x) in enumerate(zip(row, hx)):
            draw.text((x, y), val, fill=TEXT if ci < 4 else INDIGO_LIGHT, font=f12)

    # Metrics cards
    metrics = [("ACCOUNT", "$50,042"), ("DEBIT", "$349,200"), ("CREDIT", "$401,200"), ("BALANCE", "$1,559,100")]
    for i, (label, val) in enumerate(metrics):
        x = 230 + i * 295
        draw.rounded_rectangle([(x, 460), (x + 275, 510)], radius=10, fill=INDIGO_DIM, outline="#6366f120")
        draw.text((x+12, 466), label, fill=INDIGO, font=_font(9))
        draw.text((x+12, 482), val, fill=TEXT, font=b18)

    # Chart area (simplified bar chart)
    chart_x, chart_y, chart_w, chart_h = 230, 530, 1180, 250
    draw.rounded_rectangle([(chart_x, chart_y), (chart_x+chart_w, chart_y+chart_h)], radius=10, fill=CARD_BG, outline=BORDER)
    draw.text((chart_x+15, chart_y+10), "Debit by Category", fill=TEXT, font=b14)

    bars = [("COGS", 135, "#7c3aed"), ("Operating", 204, "#6366f1"), ("Other", 2, "#818cf8"), ("Revenue", 0, "#a5b4fc")]
    for i, (label, height_pct, color) in enumerate(bars):
        bx = chart_x + 100 + i * 260
        bar_h = int(height_pct * 0.9)
        bar_top = chart_y + chart_h - 40 - bar_h
        draw.rounded_rectangle([(bx, bar_top), (bx + 100, chart_y + chart_h - 40)], radius=4, fill=color)
        draw.text((bx+20, chart_y + chart_h - 30), label, fill=TEXT_DIM, font=f10)

    # Generate button
    draw.rounded_rectangle([(230, 810), (1410, 850)], radius=10, fill=INDIGO)
    draw.text((770, 822), "Generate Report", fill=WHITE, font=b14)

    # Footer
    draw.text((550, 870), "FinVault AI v3.0 - All processing runs locally. Powered by Google Gemma via LM Studio.", fill=TEXT_MUTED, font=f10)

    path = OUTPUT_DIR / "01_dashboard_report.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# 2) Data Query screenshot
# ---------------------------------------------------------------------------
def create_query_screenshot():
    W, H = 1440, 900
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f14 = _font(14); f12 = _font(12); f10 = _font(10)
    b24 = _bold(24); b18 = _bold(18); b14 = _bold(14); b12 = _bold(12)

    # Sidebar (compact)
    draw.rectangle([(0, 0), (200, H)], fill=CARD_BG)
    draw.line([(200, 0), (200, H)], fill=BORDER, width=1)
    draw.text((55, 30), "FinVault AI", fill=INDIGO_LIGHT, font=b18)
    draw.text((42, 55), "PRIVATE BY DESIGN", fill=TEXT_MUTED, font=_font(9))
    draw.rounded_rectangle([(12, 210), (188, 245)], radius=8, fill="#22c55e10", outline=GREEN_DIM)
    draw.ellipse([(20, 222), (28, 230)], fill=GREEN)
    draw.text((34, 218), "Connected", fill=GREEN, font=b12)
    draw.text((20, 234), "google/gemma-4-e4b", fill=TEXT_DIM, font=_font(8))

    # Header
    draw.rounded_rectangle([(220, 20), (1420, 120)], radius=16, fill=INDIGO_DIM, outline="#6366f125")
    draw.text((250, 35), "FinVault AI", fill=INDIGO_LIGHT, font=_bold(30))
    draw.text((250, 72), "On-device financial intelligence. Private by design.", fill=TEXT_DIM, font=f14)

    # Tabs - Data Query active
    tab_y = 140
    draw.rounded_rectangle([(220, tab_y), (620, tab_y+40)], radius=10, fill=CARD_BG, outline=BORDER)
    draw.text((244, tab_y+12), "Report Generator", fill=TEXT_DIM, font=b12)
    draw.rounded_rectangle([(360, tab_y+4), (470, tab_y+36)], radius=8, fill=INDIGO)
    draw.text((378, tab_y+12), "Data Query", fill=WHITE, font=b12)
    draw.text((484, tab_y+12), "Document OCR", fill=TEXT_DIM, font=b12)

    # Column chips
    chip_y = 200
    cols = ["Date", "Account", "Category", "Description", "Debit", "Credit", "Balance"]
    cx = 230
    for c in cols:
        w = len(c) * 8 + 20
        draw.rounded_rectangle([(cx, chip_y), (cx+w, chip_y+22)], radius=11, fill=INDIGO_DIM, outline="#6366f130")
        draw.text((cx+10, chip_y+4), c, fill=INDIGO_LIGHT, font=f10)
        cx += w + 8

    # Chat messages
    # User message
    draw.rounded_rectangle([(230, 250), (1410, 300)], radius=12, fill="#1e293b", outline="#33415540")
    draw.ellipse([(245, 265), (265, 285)], fill="#ef4444")
    draw.text((275, 268), "What is the total revenue for Q1 2026?", fill=TEXT, font=f14)

    # Assistant response
    draw.rounded_rectangle([(230, 320), (1410, 600)], radius=12, fill=CARD_BG, outline="#33415540")
    draw.ellipse([(245, 335), (265, 355)], fill=INDIGO)
    draw.text((275, 338), "The total revenue for Q1 2026 is $401,200.00.", fill=TEXT, font=b14)

    draw.text((275, 375), "Calculation Steps:", fill=INDIGO_LIGHT, font=b14)
    steps = [
        "To find total revenue for Q1 2026 (January-March), we sum all",
        "transactions categorized as 'Revenue' during this period:",
        "",
        "  1.  January Revenue:     Product Sales Q1 (2026-01-05): $125,000.00",
        "  2.  February Revenue:    Product Sales Feb (2026-02-05): $98,000.00",
        "  3.  March Revenue:       Product Sales Mar (2026-03-05): $142,000.00",
        "  4.  March Revenue:       Consulting Services (2026-03-08): $35,000.00",
        "  5.  March Other Income:  Interest Income (2026-03-30): $1,200.00",
        "",
        "  Total = $125,000 + $98,000 + $142,000 + $35,000 + $1,200",
        "  Total Revenue Q1 2026 = $401,200.00",
    ]
    sy = 400
    for line in steps:
        color = INDIGO_LIGHT if line.strip().startswith(("1.", "2.", "3.", "4.", "5.")) else TEXT_DIM if "Total" not in line else TEXT
        if "Total Revenue" in line:
            color = GREEN
        draw.text((275, sy), line, fill=color, font=f12)
        sy += 18

    # Second user message
    draw.rounded_rectangle([(230, 620), (1410, 670)], radius=12, fill="#1e293b", outline="#33415540")
    draw.ellipse([(245, 635), (265, 655)], fill="#ef4444")
    draw.text((275, 638), "Which category has the highest expenses?", fill=TEXT, font=f14)

    # Spinner
    draw.rounded_rectangle([(230, 690), (1410, 730)], radius=12, fill=CARD_BG, outline="#33415540")
    draw.ellipse([(245, 700), (265, 720)], fill=INDIGO)
    draw.text((275, 703), "Analysing ...", fill=TEXT_DIM, font=f14)

    # Chat input
    draw.rounded_rectangle([(230, 760), (1410, 800)], radius=10, fill=CARD_BG, outline=BORDER)
    draw.text((250, 773), "Ask a question about your data ...", fill=TEXT_MUTED, font=f12)
    # Send button
    draw.rounded_rectangle([(1370, 765), (1405, 795)], radius=6, fill=INDIGO)
    draw.text((1380, 773), ">", fill=WHITE, font=b14)

    # Footer
    draw.text((550, 860), "FinVault AI v3.0 - All processing runs locally. Powered by Google Gemma via LM Studio.", fill=TEXT_MUTED, font=f10)

    path = OUTPUT_DIR / "02_data_query.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# 3) OCR Processing screenshot
# ---------------------------------------------------------------------------
def create_ocr_screenshot():
    W, H = 1440, 900
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f14 = _font(14); f12 = _font(12); f10 = _font(10)
    b18 = _bold(18); b14 = _bold(14); b12 = _bold(12)

    # Sidebar (compact)
    draw.rectangle([(0, 0), (200, H)], fill=CARD_BG)
    draw.line([(200, 0), (200, H)], fill=BORDER, width=1)
    draw.text((55, 30), "FinVault AI", fill=INDIGO_LIGHT, font=b18)

    # Header
    draw.rounded_rectangle([(220, 20), (1420, 120)], radius=16, fill=INDIGO_DIM, outline="#6366f125")
    draw.text((250, 35), "FinVault AI", fill=INDIGO_LIGHT, font=_bold(30))
    draw.text((250, 72), "On-device financial intelligence. Private by design.", fill=TEXT_DIM, font=f14)

    # Tabs - OCR active
    tab_y = 140
    draw.rounded_rectangle([(220, tab_y), (620, tab_y+40)], radius=10, fill=CARD_BG, outline=BORDER)
    draw.text((244, tab_y+12), "Report Generator", fill=TEXT_DIM, font=b12)
    draw.text((378, tab_y+12), "Data Query", fill=TEXT_DIM, font=b12)
    draw.rounded_rectangle([(472, tab_y+4), (605, tab_y+36)], radius=8, fill=INDIGO)
    draw.text((486, tab_y+12), "Document OCR", fill=WHITE, font=b12)

    # Doc type
    draw.text((230, 200), "Document Type", fill=TEXT_DIM, font=f12)
    draw.rounded_rectangle([(230, 218), (420, 244)], radius=6, fill="#0f1117", outline=BORDER)
    draw.text((242, 224), "Invoice", fill=TEXT, font=f12)

    # DOC 1 label
    draw.rounded_rectangle([(230, 265), (290, 283)], radius=6, fill="#6366f120")
    draw.text((238, 268), "DOC 1", fill=INDIGO_LIGHT, font=_font(9))
    draw.text((298, 268), "sample_invoice.png", fill=TEXT, font=f12)

    # Left: invoice image thumbnail
    draw.rounded_rectangle([(230, 300), (700, 680)], radius=10, fill=CARD_BG, outline=BORDER)
    # Simplified invoice representation
    draw.rounded_rectangle([(250, 315), (680, 345)], radius=4, fill="#1a365d")
    draw.text((260, 323), "ACME CONSULTING GROUP", fill=WHITE, font=b12)
    draw.text((530, 323), "INVOICE", fill=WHITE, font=b12)
    draw.text((260, 355), "INV-2026-0847", fill=TEXT_DIM, font=f10)
    draw.text((260, 370), "March 15, 2026", fill=TEXT_DIM, font=f10)
    draw.text((260, 385), "Due: April 14, 2026", fill=TEXT_DIM, font=f10)
    draw.text((260, 405), "Bill To: TechForward Inc.", fill=TEXT, font=f10)
    # Table lines
    for i in range(6):
        y = 430 + i * 18
        draw.line([(260, y), (670, y)], fill=BORDER)
        draw.text((265, y+2), f"Service line item {i+1}" if i < 5 else "TOTAL DUE: $65,250.00", fill=TEXT_DIM if i < 5 else TEXT, font=f10)

    draw.text((260, 560), "Payment: First National Bank", fill=TEXT_DIM, font=f10)
    draw.text((260, 575), "Routing: 021000021", fill=TEXT_DIM, font=f10)

    # Right: Parsed results
    rx = 720
    # Confidence badges
    draw.rounded_rectangle([(rx, 300), (rx+100, 345)], radius=8, fill=INDIGO_DIM, outline="#6366f120")
    draw.text((rx+10, 305), "CONFIDENCE", fill=TEXT_DIM, font=_font(8))
    draw.text((rx+20, 320), "87.0%", fill=GREEN, font=b14)

    draw.rounded_rectangle([(rx+115, 300), (rx+215, 345)], radius=8, fill=INDIGO_DIM, outline="#6366f120")
    draw.text((rx+125, 305), "WORDS", fill=TEXT_DIM, font=_font(8))
    draw.text((rx+145, 320), "134", fill=INDIGO_LIGHT, font=b14)

    # Parsed data header
    draw.text((rx, 365), "PARSED STRUCTURED DATA", fill=INDIGO, font=_font(9))

    # Parsed table
    draw.rounded_rectangle([(rx, 385), (1410, 680)], radius=10, fill=CARD_BG, outline=BORDER)
    fields = [
        ("Invoice Number", "INV-2026-0847"),
        ("Invoice Date", "March 15, 2026"),
        ("Due Date", "April 14, 2026"),
        ("Payment Terms", "Net 30"),
        ("Vendor Name", "TechForward Inc."),
        ("Subtotal", "$60,000.00"),
        ("Tax (8.75%)", "$5,250.00"),
        ("Total Due", "$65,250.00"),
        ("Bank", "First National Bank"),
        ("Routing", "021000021"),
        ("Account", "4829-3371-0056"),
    ]
    fy = 395
    for field, value in fields:
        draw.text((rx+15, fy), field, fill=INDIGO_LIGHT, font=f10)
        draw.text((rx+180, fy), value, fill=TEXT, font=f12)
        fy += 24
        if fy < 670:
            draw.line([(rx+10, fy-3), (1400, fy-3)], fill="#33415530")

    # Download buttons
    draw.rounded_rectangle([(rx, 700), (rx+200, 730)], radius=8, fill=CARD_BG, outline=BORDER)
    draw.text((rx+20, 708), "Download Raw Text", fill=TEXT, font=f10)
    draw.rounded_rectangle([(rx+220, 700), (rx+440, 730)], radius=8, fill=CARD_BG, outline=BORDER)
    draw.text((rx+240, 708), "Download Parsed Data", fill=TEXT, font=f10)

    path = OUTPUT_DIR / "03_ocr_processing.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# 4) Admin Panel screenshot
# ---------------------------------------------------------------------------
def create_admin_screenshot():
    W, H = 440, 800
    img = Image.new("RGB", (W, H), CARD_BG)
    draw = ImageDraw.Draw(img)
    f12 = _font(12); f10 = _font(10); f9 = _font(9)
    b18 = _bold(18); b14 = _bold(14); b12 = _bold(12)

    # Branding
    draw.text((140, 25), "FinVault AI", fill=INDIGO_LIGHT, font=b18)
    draw.text((128, 50), "PRIVATE BY DESIGN", fill=TEXT_MUTED, font=_font(9))
    draw.rounded_rectangle([(90, 75), (350, 95)], radius=12, fill="#22c55e10", outline=GREEN_DIM)
    draw.text((100, 79), "OFFLINE  *  AIR-GAPPED  *  SECURE", fill=GREEN, font=_font(9))

    draw.line([(15, 110), (425, 110)], fill=BORDER)

    # CONNECTION
    draw.text((15, 125), "CONNECTION", fill=TEXT_DIM, font=f9)
    draw.rounded_rectangle([(15, 145), (425, 170)], radius=6, fill=BG, outline=BORDER)
    draw.text((25, 152), "http://localhost:1234/v1", fill=TEXT_DIM, font=f10)
    draw.rounded_rectangle([(15, 180), (425, 205)], radius=6, fill=BG, outline=BORDER)
    draw.text((25, 187), "google/gemma-4-e4b", fill=TEXT, font=f10)

    # Connected card
    draw.rounded_rectangle([(15, 215), (425, 260)], radius=10, fill="#22c55e10", outline=GREEN_DIM)
    draw.ellipse([(25, 228), (35, 238)], fill=GREEN)
    draw.text((42, 225), "Connected", fill=GREEN, font=b12)
    draw.text((25, 244), "google/gemma-4-e4b", fill=TEXT_DIM, font=_font(9))

    draw.line([(15, 275), (425, 275)], fill=BORDER)

    # ADMIN
    draw.text((15, 290), "ADMIN", fill=TEXT_DIM, font=f9)

    # Model & Inference (expanded)
    draw.rounded_rectangle([(15, 310), (425, 500)], radius=8, fill=CARD_BG, outline=BORDER)
    draw.text((25, 316), "Model & Inference", fill=TEXT, font=b12)

    # Model card
    draw.rounded_rectangle([(25, 340), (415, 400)], radius=8, fill=INDIGO_DIM, outline="#6366f130")
    draw.text((35, 347), "ACTIVE MODEL", fill=INDIGO, font=_font(8))
    draw.text((35, 362), "Gemma 4", fill=TEXT, font=b14)
    draw.text((35, 382), "google/gemma-4-e4b", fill=TEXT_DIM, font=_font(9))

    # Sliders
    sliders = [("Temperature", "0.15", 415), ("Max Tokens", "2048", 445), ("Top-P", "0.95", 475)]
    for label, val, y in sliders:
        draw.text((25, y), label, fill=TEXT_DIM, font=f10)
        draw.text((370, y), val, fill=INDIGO_LIGHT, font=f10)

    # System Health (expanded)
    draw.rounded_rectangle([(15, 515), (425, 620)], radius=8, fill=CARD_BG, outline=BORDER)
    draw.text((25, 521), "System Health", fill=TEXT, font=b12)

    # Health indicators
    draw.text((60, 550), "OCR ENGINE", fill=TEXT_DIM, font=_font(8))
    draw.text((70, 565), "Active", fill=GREEN, font=b14)
    draw.text((250, 550), "LLM SERVER", fill=TEXT_DIM, font=_font(8))
    draw.text((260, 565), "Online", fill=GREEN, font=b14)
    draw.text((140, 592), "ENDPOINT", fill=TEXT_DIM, font=_font(8))
    draw.text((100, 605), "http://localhost:1234/v1", fill=TEXT_DIM, font=f10)

    # About (expanded)
    draw.rounded_rectangle([(15, 635), (425, 730)], radius=8, fill=CARD_BG, outline=BORDER)
    draw.text((25, 641), "About", fill=TEXT, font=b12)
    about_lines = [
        "FinVault AI v3.0",
        "All inference runs locally via LM Studio.",
        "Zero data transmitted. Zero cloud dependencies.",
        "Designed for financial professionals.",
    ]
    ay = 665
    for line in about_lines:
        color = TEXT if "FinVault" in line else INDIGO_LIGHT if "Designed" in line else TEXT_DIM
        draw.text((25, ay), line, fill=color, font=f10)
        ay += 16

    path = OUTPUT_DIR / "04_admin_panel.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# 5) Architecture Diagram
# ---------------------------------------------------------------------------
def create_architecture_diagram():
    W, H = 1200, 700
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f12 = _font(12); f10 = _font(10); f9 = _font(9)
    b18 = _bold(18); b14 = _bold(14); b12 = _bold(12)

    draw.text((430, 15), "FinVault AI — System Architecture", fill=INDIGO_LIGHT, font=b18)

    # Security boundary
    draw.rounded_rectangle([(30, 55), (1170, 670)], radius=16, outline=GREEN, width=2)
    draw.text((50, 60), "LOCAL MACHINE — AIR-GAPPED BOUNDARY", fill=GREEN, font=_font(9))

    # User layer
    draw.rounded_rectangle([(60, 100), (280, 200)], radius=10, fill=INDIGO_DIM, outline=INDIGO)
    draw.text((110, 110), "USER", fill=INDIGO, font=_font(9))
    draw.text((90, 135), "Web Browser", fill=TEXT, font=b14)
    draw.text((90, 160), "localhost:8501", fill=TEXT_DIM, font=f10)

    # Arrow
    draw.line([(280, 150), (370, 150)], fill=INDIGO_LIGHT, width=2)
    draw.polygon([(370, 145), (370, 155), (380, 150)], fill=INDIGO_LIGHT)

    # Streamlit App
    draw.rounded_rectangle([(380, 80), (780, 220)], radius=12, fill=CARD_BG, outline=INDIGO)
    draw.text((420, 88), "STREAMLIT APPLICATION", fill=INDIGO, font=_font(9))
    draw.text((400, 115), "app.py", fill=TEXT, font=b14)

    # Sub-modules
    modules = [("Report Gen", 400, 145), ("Data Query", 530, 145), ("OCR Engine", 660, 145)]
    for label, x, y in modules:
        draw.rounded_rectangle([(x, y), (x+110, y+28)], radius=6, fill=INDIGO_DIM, outline="#6366f140")
        draw.text((x+10, y+6), label, fill=INDIGO_LIGHT, font=f10)

    draw.text((400, 185), "UI Layer  |  Core Logic  |  Config", fill=TEXT_DIM, font=f10)

    # Arrow to LM Studio
    draw.line([(780, 150), (860, 150)], fill=INDIGO_LIGHT, width=2)
    draw.polygon([(860, 145), (860, 155), (870, 150)], fill=INDIGO_LIGHT)
    draw.text((790, 130), "OpenAI API", fill=TEXT_DIM, font=_font(8))

    # LM Studio
    draw.rounded_rectangle([(870, 90), (1140, 210)], radius=12, fill=CARD_BG, outline="#7c3aed")
    draw.text((920, 98), "LM STUDIO", fill="#7c3aed", font=_font(9))
    draw.text((900, 125), "Gemma 4", fill=TEXT, font=b18)
    draw.text((900, 155), "google/gemma-4-e4b", fill=TEXT_DIM, font=f10)
    draw.text((900, 175), "localhost:1234", fill=TEXT_DIM, font=f10)

    # Tesseract
    draw.rounded_rectangle([(380, 270), (600, 370)], radius=12, fill=CARD_BG, outline=AMBER)
    draw.text((420, 278), "TESSERACT OCR", fill=AMBER, font=_font(9))
    draw.text((400, 305), "Text Extraction", fill=TEXT, font=b14)
    draw.text((400, 330), "Local binary", fill=TEXT_DIM, font=f10)

    # Arrow from app to Tesseract
    draw.line([(580, 220), (490, 270)], fill=AMBER, width=2)

    # Data files
    draw.rounded_rectangle([(660, 270), (900, 370)], radius=12, fill=CARD_BG, outline="#22d3ee")
    draw.text((700, 278), "LOCAL DATA", fill="#22d3ee", font=_font(9))
    draw.text((680, 305), "CSV / Excel files", fill=TEXT, font=b12)
    draw.text((680, 330), "Invoice images", fill=TEXT_DIM, font=f10)
    draw.text((680, 345), "Work-order scans", fill=TEXT_DIM, font=f10)

    # Arrow from app to data
    draw.line([(580, 220), (780, 270)], fill="#22d3ee", width=2)

    # Security callouts
    draw.rounded_rectangle([(60, 420), (560, 640)], radius=12, fill=CARD_BG, outline=GREEN)
    draw.text((80, 428), "SECURITY ARCHITECTURE", fill=GREEN, font=_font(9))
    security_items = [
        ("No network egress", "All API calls to localhost only"),
        ("No cloud dependencies", "LLM runs entirely on-device"),
        ("No data persistence", "Session-only, no server-side storage"),
        ("No telemetry", "Browser stats collection disabled"),
        ("Air-gap compatible", "Works with zero internet access"),
        ("Input validation", "File type & size limits enforced"),
    ]
    sy = 455
    for title, desc in security_items:
        draw.ellipse([(85, sy+3), (93, sy+11)], fill=GREEN)
        draw.text((102, sy), title, fill=TEXT, font=b12)
        draw.text((102, sy+16), desc, fill=TEXT_DIM, font=f10)
        sy += 35

    # Data flow
    draw.rounded_rectangle([(600, 420), (1140, 640)], radius=12, fill=CARD_BG, outline=INDIGO)
    draw.text((620, 428), "DATA FLOW", fill=INDIGO, font=_font(9))
    flow_steps = [
        "1. User uploads data via browser (localhost)",
        "2. Streamlit processes file in-memory (Python)",
        "3. Data formatted into prompt context",
        "4. Prompt sent to LM Studio (localhost:1234)",
        "5. Gemma 4 generates response locally",
        "6. Response rendered in browser",
        "7. OCR: Tesseract extracts text locally",
        "8. Parsed text sent to Gemma for structuring",
        "",
        "No data touches external servers at any point.",
    ]
    fy = 452
    for step in flow_steps:
        color = GREEN if "No data" in step else INDIGO_LIGHT if step and step[0].isdigit() else TEXT_DIM
        draw.text((620, fy), step, fill=color, font=f10)
        fy += 19

    path = OUTPUT_DIR / "05_architecture.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# 6) Roadmap Diagram
# ---------------------------------------------------------------------------
def create_roadmap_diagram():
    W, H = 1200, 600
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    f12 = _font(12); f10 = _font(10)
    b18 = _bold(18); b14 = _bold(14); b12 = _bold(12)

    draw.text((430, 15), "FinVault AI — Product Roadmap", fill=INDIGO_LIGHT, font=b18)

    phases = [
        ("Q2 2026", "Foundation", INDIGO, [
            "Report Generation",
            "NL Data Query",
            "OCR + Parsing",
            "Tesseract Integration",
            "Dark Theme UI",
            "Admin Panel",
        ]),
        ("Q3 2026", "Intelligence", "#7c3aed", [
            "RAG Pipeline",
            "Vector Store (local)",
            "Multi-doc analysis",
            "Anomaly detection",
            "Auto-categorization",
            "Chart generation",
        ]),
        ("Q4 2026", "Enterprise", "#22d3ee", [
            "Role-based access",
            "Audit logging",
            "Export to PDF/XLSX",
            "Batch processing",
            "Custom prompts",
            "Model fine-tuning",
        ]),
        ("Q1 2027", "Scale", GREEN, [
            "Multi-model support",
            "Observability dashboard",
            "Plugin architecture",
            "CI/CD pipeline",
            "Automated testing",
            "Performance profiling",
        ]),
    ]

    # Timeline line
    draw.line([(60, 85), (1140, 85)], fill=BORDER, width=2)

    for i, (quarter, title, color, items) in enumerate(phases):
        x = 60 + i * 280
        # Timeline dot
        draw.ellipse([(x+100, 78), (x+112, 90)], fill=color)

        draw.text((x+75, 55), quarter, fill=color, font=b12)

        # Phase card
        draw.rounded_rectangle([(x, 105), (x+260, 560)], radius=12, fill=CARD_BG, outline=color)
        draw.text((x+15, 115), title.upper(), fill=color, font=_font(9))

        iy = 145
        for item in items:
            draw.ellipse([(x+20, iy+5), (x+28, iy+13)], fill=color)
            draw.text((x+36, iy), item, fill=TEXT, font=f12)
            iy += 35

        # Status indicator
        if i == 0:
            draw.rounded_rectangle([(x+15, 530), (x+100, 548)], radius=8, fill=f"{color}30")
            draw.text((x+25, 534), "CURRENT", fill=color, font=_font(9))
        else:
            draw.rounded_rectangle([(x+15, 530), (x+100, 548)], radius=8, fill="#33415530")
            draw.text((x+25, 534), "PLANNED", fill=TEXT_DIM, font=_font(9))

    path = OUTPUT_DIR / "06_roadmap.png"
    img.save(path, "PNG")
    print(f"  Created: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Generating documentation screenshots ...")
    create_dashboard_screenshot()
    create_query_screenshot()
    create_ocr_screenshot()
    create_admin_screenshot()
    create_architecture_diagram()
    create_roadmap_diagram()
    print("Done! All screenshots in docs/screenshots/")
