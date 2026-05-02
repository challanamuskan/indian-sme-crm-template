"""
pages/10_Compliance.py
GST filing deadlines, TDS, Income Tax, MSME compliance tracker.
"""

import streamlit as st
if not st.session_state.get("authenticated", False):
    st.error("\U0001f512 Please login first.")
    st.stop()

import streamlit as st
import calendar
from datetime import date
from utils.config_loader import load_config

cfg = load_config()
st.title("⚖️ Govt Compliance Tracker")
st.caption("Stay ahead of GST, TDS, and Income Tax deadlines.")

today = date.today()
MONTH = today.month
YEAR  = today.year

def safe_date(year, month, day):
    """Return date clamped to last valid day of month."""
    max_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, max_day))

def days_left(d: date) -> int:
    return (d - today).days

COMPLIANCE_CALENDAR = [
    {"name": "GSTR-1 (Monthly)",        "due": safe_date(YEAR, MONTH, 11), "category": "GST",         "desc": "Outward supplies return"},
    {"name": "GSTR-3B (Monthly)",        "due": safe_date(YEAR, MONTH, 20), "category": "GST",         "desc": "Summary return + tax payment"},
    {"name": "GSTR-2B Reconciliation",   "due": safe_date(YEAR, MONTH, 14), "category": "GST",         "desc": "ITC reconciliation deadline"},
    {"name": "TDS Payment",              "due": safe_date(YEAR, MONTH, 7),  "category": "TDS",         "desc": "Deposit TDS deducted this month"},
    {"name": "TDS Return (Form 26Q)",    "due": safe_date(YEAR, MONTH, 30), "category": "TDS",         "desc": "Quarterly TDS return"},
    {"name": "Advance Tax Q1",           "due": date(YEAR, 6, 15),          "category": "Income Tax",  "desc": "15% of annual tax liability"},
    {"name": "Advance Tax Q2",           "due": date(YEAR, 9, 15),          "category": "Income Tax",  "desc": "45% of annual tax liability"},
    {"name": "Advance Tax Q3",           "due": date(YEAR, 12, 15),         "category": "Income Tax",  "desc": "75% of annual tax liability"},
    {"name": "Advance Tax Q4",           "due": date(YEAR + 1, 3, 15),      "category": "Income Tax",  "desc": "100% of annual tax liability"},
]

st.subheader("📅 This Month's Deadlines")
urgent, upcoming, done = [], [], []
for item in COMPLIANCE_CALENDAR:
    d = days_left(item["due"])
    if d < 0:
        done.append(item)
    elif d <= 7:
        urgent.append(item)
    else:
        upcoming.append(item)

if urgent:
    st.error(f"🚨 {len(urgent)} deadline(s) within 7 days!")
    for item in sorted(urgent, key=lambda x: x["due"]):
        d = days_left(item["due"])
        st.markdown(f"**{item['name']}** — Due **{item['due'].strftime('%d %b')}** ({abs(d)} days away) · _{item['desc']}_")

if upcoming:
    st.warning(f"⏰ {len(upcoming)} upcoming deadline(s)")
    for item in sorted(upcoming, key=lambda x: x["due"]):
        d = days_left(item["due"])
        st.markdown(f"**{item['name']}** — Due {item['due'].strftime('%d %b')} ({d} days) · _{item['desc']}_")

with st.expander("✅ Past deadlines this year"):
    for item in sorted(done, key=lambda x: x["due"], reverse=True):
        st.markdown(f"~~{item['name']}~~ — {item['due'].strftime('%d %b')}")

st.divider()

# ── e-Way Bill checker ────────────────────────────────────────────────────────
st.subheader("🚚 e-Way Bill Quick Check")
col1, col2 = st.columns(2)
inv_val  = col1.number_input("Invoice Value (₹)", min_value=0, step=1000)
distance = col2.number_input("Distance (km)", min_value=0)
if inv_val:
    if inv_val >= 50000:
        st.warning("⚠️ e-Way bill **required** (value ≥ ₹50,000). Generate at einvoice1.gst.gov.in")
    else:
        st.success("✅ e-Way bill not required (value < ₹50,000)")

st.divider()

# ── GST Rate finder ───────────────────────────────────────────────────────────
st.subheader("🔍 GST Rate Finder")
st.caption("Common HSN codes for SMEs")
HSN_RATES = {
    "Cotton Fabric (5208)":     "5%",
    "Polyester Fabric (5407)":  "12%",
    "Bearings (8482)":          "18%",
    "Pulleys / Gears (8483)":   "18%",
    "Motors (8501)":            "18%",
    "FMCG / Food items":        "0–12%",
    "Pharma / Medicines":       "5–12%",
    "Steel / Iron articles":    "18%",
    "Plastic goods":            "18%",
    "Stationery / Paper":       "12–18%",
}
search = st.text_input("Search product / HSN code")
for item, rate in HSN_RATES.items():
    if not search or search.lower() in item.lower():
        col_a, col_b = st.columns([3, 1])
        col_a.markdown(f"**{item}**")
        col_b.markdown(f"`{rate}`")
