"""
pages/13_Smart_Reminders.py
AI-powered business reminders: overdue payments, reorder alerts, follow-up nudges.
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.db import get_all_records
from utils.config_loader import load_config

cfg = load_config()
st.title("🔔 Smart Reminders")
st.caption("AI-generated action items based on your live business data.")

try:
    payments = get_all_records("payments")
    products = get_all_records("products")
    customers = get_all_records("customers")
    campaigns = get_all_records("campaigns", order_col="start_date")

    today = date.today()
    reminders = []

    # ── Overdue payments ──────────────────────────────────────────────────────
    for p in payments:
        if p.get("status") == "pending" and p.get("due_date"):
            due = date.fromisoformat(str(p["due_date"]))
            days_overdue = (today - due).days
            if days_overdue > 0:
                reminders.append({
                    "priority": "🔴 High",
                    "category": "Payment",
                    "action": f"Follow up on ₹{float(p['amount']):,.0f} overdue by {days_overdue} days",
                    "suggestion": "Send WhatsApp reminder or call customer today.",
                })
            elif days_overdue > -3:
                reminders.append({
                    "priority": "🟡 Medium",
                    "category": "Payment",
                    "action": f"Payment of ₹{float(p['amount']):,.0f} due in {abs(days_overdue)} days",
                    "suggestion": "Send a friendly WhatsApp reminder now.",
                })

    # ── Low stock reorder ─────────────────────────────────────────────────────
    threshold = cfg["display"]["low_stock_threshold"]
    for p in products:
        qty = int(p.get("quantity", 99))
        if qty < threshold:
            reminders.append({
                "priority": "🟡 Medium" if qty > 3 else "🔴 High",
                "category": "Stock",
                "action": f"Reorder **{p['name']}** — only {qty} {p.get('unit','pcs')} left",
                "suggestion": f"Contact supplier: {p.get('supplier','—')}",
            })

    # ── Campaign ending soon ──────────────────────────────────────────────────
    for c in campaigns:
        if c.get("end_date"):
            end = date.fromisoformat(str(c["end_date"]))
            days_left = (end - today).days
            if 0 <= days_left <= 3:
                reminders.append({
                    "priority": "🟢 Low",
                    "category": "Marketing",
                    "action": f"Campaign **{c['name']}** ends in {days_left} day(s)",
                    "suggestion": "Review ROI and decide whether to extend.",
                })

    # ── Compliance nudges (always show) ──────────────────────────────────────
    from datetime import date as d_
    import calendar as cal_
    max_day = cal_.monthrange(today.year, today.month)[1]
    gstr1_due = d_(today.year, today.month, min(11, max_day))
    days_to_gstr1 = (gstr1_due - today).days
    if 0 <= days_to_gstr1 <= 7:
        reminders.append({
            "priority": "🔴 High",
            "category": "Compliance",
            "action": f"GSTR-1 due in {days_to_gstr1} days ({gstr1_due.strftime('%d %b')})",
            "suggestion": "File on gstn.gov.in before the deadline to avoid penalty.",
        })

    # ── Display ───────────────────────────────────────────────────────────────
    if not reminders:
        st.success("🎉 No urgent reminders right now! Business looks healthy.")
    else:
        high   = [r for r in reminders if "High" in r["priority"]]
        medium = [r for r in reminders if "Medium" in r["priority"]]
        low    = [r for r in reminders if "Low" in r["priority"]]

        if high:
            st.error(f"🚨 {len(high)} urgent action(s) needed")
            for r in high:
                with st.container(border=True):
                    st.markdown(f"**{r['category']}** — {r['action']}")
                    st.caption(f"💡 {r['suggestion']}")

        if medium:
            st.warning(f"⏰ {len(medium)} item(s) to watch")
            for r in medium:
                with st.container(border=True):
                    st.markdown(f"**{r['category']}** — {r['action']}")
                    st.caption(f"💡 {r['suggestion']}")

        if low:
            with st.expander(f"ℹ️ {len(low)} low-priority reminder(s)"):
                for r in low:
                    st.markdown(f"**{r['category']}** — {r['action']}")
                    st.caption(f"💡 {r['suggestion']}")

    st.divider()

    # ── Business health score ─────────────────────────────────────────────────
    st.subheader("🏥 Business Health Score")
    score = 100
    issues = []
    if any("High" in r["priority"] and r["category"] == "Payment" for r in reminders):
        score -= 20; issues.append("Overdue payments")
    if any("High" in r["priority"] and r["category"] == "Stock" for r in reminders):
        score -= 15; issues.append("Critical low stock")
    if any(r["category"] == "Compliance" for r in reminders):
        score -= 15; issues.append("Compliance deadline approaching")

    colour = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
    st.metric(f"{colour} Health Score", f"{score}/100")
    if issues:
        st.caption("Areas needing attention: " + ", ".join(issues))
    else:
        st.caption("All systems healthy!")

except Exception as e:
    st.error(f"Could not load data: {e}")
    st.caption("Ensure SUPABASE_URL and SUPABASE_KEY are set in Streamlit secrets.")
