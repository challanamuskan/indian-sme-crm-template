"""
pages/12_WhatsApp_Orders.py
Parse WhatsApp chat export -> extract orders -> save to DB.
The most-used feature for Indian SMEs.
"""

import streamlit as st
import re
import pandas as pd
from datetime import datetime
from utils.config_loader import load_config

cfg = load_config()
st.title("📱 WhatsApp Order Importer")
st.caption("Upload a WhatsApp chat export — auto-extract customer names, orders, and amounts.")

st.info("""
**How to export a WhatsApp chat:**
1. Open the chat → tap ⋮ (3 dots) → More → Export Chat
2. Choose **Without Media**
3. Save the .txt file → upload below
""")

uploaded = st.file_uploader("Upload WhatsApp chat (.txt)", type=["txt"])

def parse_whatsapp(content: str) -> list[dict]:
    """Extract messages from WhatsApp export (Android + iOS format)."""
    # Android: 15/03/2024, 10:23 - Name: message
    # iOS:     [15/03/2024, 10:23:45] Name: message
    pattern = r'(?:\[)?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}),?\s*(\d{1,2}:\d{2}(?::\d{2})?(?:\s*[AP]M)?)(?:\])?[\s\-–]+([^:]+):\s*(.+)'
    messages = []
    for line in content.splitlines():
        m = re.match(pattern, line.strip())
        if m:
            messages.append({
                "date": m.group(1),
                "time": m.group(2),
                "sender": m.group(3).strip(),
                "message": m.group(4).strip(),
            })
    return messages

def extract_order_signals(messages: list[dict]) -> list[dict]:
    """Flag messages that look like orders."""
    order_keywords = ["chahiye", "order", "need", "want", "send", "qty", "quantity",
                      "piece", "pcs", "kg", "meter", "mtr", "nos", "box", "pack",
                      "urgent", "asap", "jaldi", "book", "confirm"]
    amount_pattern = re.compile(r'[₹rs\.]{0,3}\s*(\d[\d,]*(?:\.\d{2})?)', re.IGNORECASE)
    results = []
    for msg in messages:
        text = msg["message"].lower()
        is_order = any(kw in text for kw in order_keywords)
        amounts  = amount_pattern.findall(msg["message"])
        amount   = float(amounts[0].replace(",", "")) if amounts else None
        if is_order or amount:
            results.append({
                "date":    msg["date"],
                "sender":  msg["sender"],
                "message": msg["message"],
                "amount":  amount,
                "flagged": is_order,
            })
    return results

if uploaded:
    content = uploaded.read().decode("utf-8", errors="ignore")
    messages = parse_whatsapp(content)

    if not messages:
        st.error("Could not parse this file. Make sure it's a WhatsApp .txt export.")
        st.stop()

    st.success(f"✅ Parsed {len(messages)} messages")

    orders = extract_order_signals(messages)
    st.info(f"Found **{len(orders)} potential orders** out of {len(messages)} messages")

    if orders:
        df = pd.DataFrame(orders)
        df["amount"] = df["amount"].apply(lambda x: f"₹{x:,.0f}" if x else "—")
        df["flagged"] = df["flagged"].map({True: "🛒 Order", False: "💰 Amount only"})
        df.columns = ["Date", "Customer", "Message", "Amount", "Type"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        if st.button("💾 Save customers to CRM", type="primary"):
            unique_senders = list({o["Customer"] for o in orders if "business" not in o["Customer"].lower()})
            st.success(f"Would save {len(unique_senders)} customers. Wire to insert_record('customers') in db.py.")
            st.caption("Trump card: actual DB insert logic lives in utils/db.py — not shown here.")

    # raw preview
    with st.expander(f"All {len(messages)} messages"):
        df_all = pd.DataFrame(messages)
        st.dataframe(df_all, use_container_width=True, hide_index=True)
