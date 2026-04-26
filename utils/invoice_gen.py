"""
utils/invoice_gen.py — GST Invoice PDF Generator
Generates compliant GST tax invoices as PDF using ReportLab.
Output: bytes (write to file or return via st.download_button)
"""

from __future__ import annotations
from datetime import datetime
from utils.config_loader import load_config

# ReportLab required: pip install reportlab
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

import io


def generate_gst_invoice(order: dict, line_items: list[dict]) -> bytes:
    """
    Generate a GST-compliant invoice PDF.

    Args:
        order: {customer_name, customer_gstin, invoice_no, date, ...}
        line_items: [{description, hsn, qty, unit, rate, gst_pct}, ...]

    Returns:
        PDF as bytes — use with st.download_button(data=bytes, ...)
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab not installed. Run: pip install reportlab")

    cfg = load_config()
    biz = cfg["business"]
    buf = io.BytesIO()

    doc = SimpleDocTemplate(buf, pagesize=A4,
                            topMargin=30, bottomMargin=30,
                            leftMargin=40, rightMargin=40)
    styles = getSampleStyleSheet()
    elements = []

    # ── Header ────────────────────────────────────────────
    elements.append(Paragraph(f"<b>{biz['name']}</b>", styles["Title"]))
    elements.append(Paragraph(
        f"{biz['address_line1']}, {biz['city']}, {biz['state']} — {biz['pincode']}<br/>"
        f"GSTIN: {biz['gstin']} | Ph: {biz['phone']}",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b>TAX INVOICE</b>", styles["Heading2"]))

    # ── Invoice meta ──────────────────────────────────────
    meta = [
        ["Invoice No:", order.get("invoice_no", ""), "Date:", order.get("date", datetime.today().strftime("%d-%m-%Y"))],
        ["Bill To:", order.get("customer_name", ""), "GSTIN:", order.get("customer_gstin", "N/A")],
    ]
    t = Table(meta, colWidths=[80, 200, 60, 150])
    t.setStyle(TableStyle([("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                            ("FONTSIZE", (0, 0), (-1, -1), 9)]))
    elements.append(t)
    elements.append(Spacer(1, 10))

    # ── Line items ────────────────────────────────────────
    headers = ["#", "Description", "HSN", "Qty", "Unit", "Rate (₹)", "GST%", "Amount (₹)"]
    rows = [headers]
    subtotal = 0.0
    total_gst = 0.0

    for i, item in enumerate(line_items, 1):
        rate = float(item.get("rate", 0))
        qty = float(item.get("qty", 0))
        gst_pct = float(item.get("gst_pct", cfg["gst"]["default_rate"]))
        base = rate * qty
        gst_amt = base * gst_pct / 100
        subtotal += base
        total_gst += gst_amt
        rows.append([
            str(i),
            item.get("description", ""),
            item.get("hsn", ""),
            str(qty),
            item.get("unit", "Nos"),
            f"{rate:.2f}",
            f"{gst_pct}%",
            f"{base + gst_amt:.2f}",
        ])

    rows.append(["", "", "", "", "", "", "Subtotal", f"{subtotal:.2f}"])
    rows.append(["", "", "", "", "", "", "GST Total", f"{total_gst:.2f}"])
    rows.append(["", "", "", "", "", "", "GRAND TOTAL", f"{subtotal + total_gst:.2f}"])

    t2 = Table(rows, colWidths=[20, 150, 50, 30, 40, 60, 50, 80])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -4), [colors.white, colors.lightyellow]),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Authorised Signatory: ___________________", styles["Normal"]))
    elements.append(Paragraph("<i>This is a computer-generated invoice.</i>", styles["Normal"]))

    doc.build(elements)
    return buf.getvalue()
