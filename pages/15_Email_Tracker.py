"""pages/15_Email_Tracker.py — Email outreach log, follow-up tracker, templates."""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.config_loader import load_config

cfg = load_config()
st.title("📧 Email & Follow-up Tracker")
st.caption("Log outreach, track replies, set follow-up reminders.")

# ── Gmail compose shortcuts ───────────────────────────────────────────────────
st.subheader("✉️ Quick Compose")
tab1, tab2, tab3 = st.tabs(["Payment Reminder", "Order Confirmation", "Custom"])

TEMPLATES = {
    "Payment Reminder": """Subject: Payment Reminder — Invoice #{invoice_no}

Dear {customer_name},

This is a friendly reminder that payment of {currency}{amount} for Invoice #{invoice_no} 
was due on {due_date}.

Kindly arrange payment at your earliest convenience via:
• UPI: {upi_id}
• Bank: {bank_details}

Please ignore if already paid.

Regards,
{business_name}""",

    "Order Confirmation": """Subject: Order Confirmed — #{order_id}

Dear {customer_name},

Thank you for your order! Here's your order summary:

Order ID: #{order_id}
Items: {items}
Total: {currency}{amount}
Expected Delivery: {delivery_date}

We'll notify you when your order is dispatched.

Regards,
{business_name}""",
}

with tab1:
    st.text_area("Payment Reminder Template", TEMPLATES["Payment Reminder"], height=250)
    col1, col2, col3 = st.columns(3)
    to_email   = col1.text_input("To (email)")
    inv_no     = col2.text_input("Invoice #")
    amount     = col3.number_input(f"Amount ({cfg['business']['currency']})", min_value=0.0)
    if st.button("Open in Gmail", key="pay_rem"):
        subject = f"Payment Reminder — Invoice #{inv_no}"
        body    = f"Dear Customer,%0A%0APayment of {cfg['business']['currency']}{amount} for Invoice #{inv_no} is due. Please arrange payment at the earliest.%0A%0ARegards,%0A{cfg['business']['name']}"
        gmail_url = f"https://mail.google.com/mail/?view=cm&to={to_email}&su={subject}&body={body}"
        st.markdown(f"[📧 Open Gmail Draft]({gmail_url})", unsafe_allow_html=True)

with tab2:
    st.text_area("Order Confirmation Template", TEMPLATES["Order Confirmation"], height=250)
    st.caption("Customise and use as a base for order confirmations.")

with tab3:
    subject = st.text_input("Subject")
    to      = st.text_input("To")
    body    = st.text_area("Body", height=200)
    if st.button("Open in Gmail", key="custom"):
        url = f"https://mail.google.com/mail/?view=cm&to={to}&su={subject}&body={body.replace(chr(10),'%0A')}"
        st.markdown(f"[📧 Open Gmail]({url})", unsafe_allow_html=True)

st.divider()

# ── Follow-up log ─────────────────────────────────────────────────────────────
st.subheader("📋 Follow-up Log")
st.caption("Track who needs a follow-up and when.")

if "followups" not in st.session_state:
    st.session_state.followups = [
        {"contact": "Ramesh Traders", "topic": "Payment ₹12,500", "due": str(date.today()), "status": "Pending"},
        {"contact": "Priya Stores",   "topic": "Order confirmation", "due": str(date.today() + timedelta(days=2)), "status": "Pending"},
    ]

with st.expander("➕ Add Follow-up"):
    c1, c2 = st.columns(2)
    contact = c1.text_input("Contact / Customer")
    topic   = c2.text_input("Topic")
    due     = c1.date_input("Follow-up Date", value=date.today() + timedelta(days=1))
    if st.button("Add"):
        st.session_state.followups.append({"contact":contact,"topic":topic,"due":str(due),"status":"Pending"})
        st.rerun()

df_fu = pd.DataFrame(st.session_state.followups)
if not df_fu.empty:
    df_fu["due"] = pd.to_datetime(df_fu["due"])
    today_dt = pd.Timestamp(date.today())
    df_fu["Urgency"] = df_fu["due"].apply(lambda d: "🔴 Overdue" if d < today_dt else ("🟡 Today" if d == today_dt else "🟢 Upcoming"))
    df_fu = df_fu.sort_values("due")
    st.dataframe(df_fu[["contact","topic","due","status","Urgency"]].rename(
        columns={"contact":"Contact","topic":"Topic","due":"Due Date","status":"Status"}),
        use_container_width=True, hide_index=True)
