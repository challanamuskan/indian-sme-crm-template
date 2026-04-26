"""
pages/10_Compliance.py
GST filing deadlines, TDS dates, MSME, and custom compliance reminders.
"""

import streamlit as st
from datetime import date, datetime
from utils.config_loader import load_config
from utils.db import get_all_records, insert_record

cfg = load_config()

st.title("⚖️ Govt Compliance Tracker")
st.caption("Stay ahead of GST, TDS, and MSME deadlines.")

# ── Standard Indian compliance calendar ─────────────────────────────────────
today = date.today()
MONTH = today.month
YEAR = today.year

def days_left(d: date) -> int:
    return (d - today).days

COMPLIANCE_CALENDAR = [
    # GST
    {"name": "GSTR-1 (Monthly)", "due": date(YEAR, MONTH, 11), "category": "GST", "desc": "Outward supplies"},
    {"name": "GSTR-3B (Monthly)", "due": date(YEAR, MONTH, 20), "category": "GST", "desc": "Summary return + tax payment"},
    {"name": "GSTR-2B Reconciliation", "due": date(YEAR, MONTH, 14), "category": "GST", "desc": "ITC reconciliation"},
    # TDS
    {"name": "TDS Payment (Quarterly)", "due": date(YEAR, MONTH, 7), "category": "TDS", "desc": "Deposit TDS deducted"},
    {"name": "TDS Return (Form 26Q)", "due": date(YEAR, MONTH, 31), "category": "TDS", "desc": "Quarterly TDS return"},
    # Income Tax
    {"name": "Advance Tax (Q1)", "due": date(YEAR, 6, 15), "category": "Income Tax", "desc": "15% of annual tax liability"},
    {"name": "Advance Tax (Q2)", "due": date(YEAR, 9, 15), "category": "Income Tax", "desc": "45% of annual tax liability"},
    {"name": "Advance Tax (Q3)", "due": date(YEAR, 12, 15), "category": "Income Tax", "desc": "75% of annual tax liability"},
    {"name": "Advance Tax (Q4)", "due": date(YEAR + 1, 3, 15), "category": "Income Tax", "desc": "100% of annual tax liability"},
]

st.subheader("📅 Compliance Calendar — This Month")
for item in sorted(COMPLIANCE_CALENDAR, key=lambda x: x["due"]):
    dl = days_left(item["due"])
    if dl < 0:
        status = "✅ Done / Passed"
        color = "green"
    elif dl <= 3:
        status = f"🔴 DUE IN {dl} DAYS"
        color = "red"
    elif dl <= 7:
        status = f"🟠 Due in {dl} days"
        color = "orange"
    else:
        status = f"🟢 {dl} days left"
        color = "normal"

    with st.container():
        c1, c2, c3 = st.columns([3, 2, 2])
        c1.markdown(f"**{item['name']}** — _{item['desc']}_")
        c2.markdown(f"`{item['due'].strftime('%d %b %Y')}`")
        c3.markdown(f":{color}[{status}]" if color != "normal" else status)
    st.divider()

# ── Custom reminders ─────────────────────────────────────────────────────────
st.subheader("➕ Custom Compliance Reminder")
with st.expander("Add custom reminder"):
    r_name = st.text_input("Reminder name")
    r_date = st.date_input("Due date")
    r_note = st.text_area("Notes")
    if st.button("Save Reminder"):
        insert_record("compliance_reminders", {
            "name": r_name, "due_date": str(r_date), "notes": r_note, "done": False
        })
        st.success("Reminder saved!")
        st.rerun()

reminders = get_all_records("compliance_reminders", order_col="due_date")
if reminders:
    st.subheader("Your Custom Reminders")
    for r in reminders:
        st.write(f"📌 **{r['name']}** — {r['due_date']} {'✅' if r.get('done') else '⏳'}")
