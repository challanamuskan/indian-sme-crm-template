"""
pages/6_GST_Invoices.py
Create, preview, and download GST-compliant invoices as PDF.
"""

import streamlit as st
if not st.session_state.get("authenticated", False):
    st.error("\U0001f512 Please login first.")
    st.stop()

import streamlit as st
from datetime import date
from utils.config_loader import load_config
from utils.db import get_all_records, insert_record
from utils.invoice_gen import generate_gst_invoice

cfg = load_config()
biz = cfg["business"]

st.title("🧾 GST Invoice Generator")
st.caption(f"GSTIN: {biz['gstin']} | {biz['name']}")

# ── Invoice form ────────────────────────────────────────────────────────────
with st.expander("➕ Create New Invoice", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.text_input("Customer / Party Name")
        customer_gstin = st.text_input("Customer GSTIN (optional)")
        invoice_no = st.text_input("Invoice No.", placeholder="e.g. INV-2025-001")
    with col2:
        invoice_date = st.date_input("Invoice Date", value=date.today())
        payment_terms = st.selectbox("Payment Terms", ["Immediate", "7 Days", "15 Days", "30 Days"])

    st.markdown("**Line Items**")
    n_items = st.number_input("Number of items", min_value=1, max_value=20, value=1)

    line_items = []
    for i in range(int(n_items)):
        c1, c2, c3, c4, c5, c6 = st.columns([3, 1, 1, 1, 1, 1])
        with c1: desc = st.text_input(f"Description #{i+1}", key=f"desc_{i}")
        with c2: hsn = st.text_input("HSN", key=f"hsn_{i}")
        with c3: qty = st.number_input("Qty", min_value=0.0, key=f"qty_{i}")
        with c4: unit = st.selectbox("Unit", ["Nos", "Kg", "Mtr", "Set", "Pair"], key=f"unit_{i}")
        with c5: rate = st.number_input("Rate ₹", min_value=0.0, key=f"rate_{i}")
        with c6: gst_pct = st.number_input("GST%", min_value=0, max_value=28, value=18, key=f"gst_{i}")
        line_items.append({"description": desc, "hsn": hsn, "qty": qty,
                            "unit": unit, "rate": rate, "gst_pct": gst_pct})

    if st.button("Generate Invoice PDF", type="primary"):
        order = {
            "customer_name": customer_name,
            "customer_gstin": customer_gstin,
            "invoice_no": invoice_no,
            "date": invoice_date.strftime("%d-%m-%Y"),
        }
        try:
            pdf_bytes = generate_gst_invoice(order, line_items)
            st.download_button(
                label="⬇️ Download Invoice PDF",
                data=pdf_bytes,
                file_name=f"{invoice_no or 'invoice'}.pdf",
                mime="application/pdf",
            )
            st.success("Invoice generated!")
        except ImportError:
            st.error("ReportLab not installed. Run: `pip install reportlab`")

# ── Past invoices table ─────────────────────────────────────────────────────
st.divider()
st.subheader("Past Invoices")
invoices = get_all_records("invoices")
if invoices:
    st.dataframe(invoices, use_container_width=True)
else:
    st.info("No invoices yet. Create one above.")
