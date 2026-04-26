"""
pages/8_Ad_Tracker.py
Track marketing campaigns — budget, platform, reach, leads, ROI.
"""

import streamlit as st
import pandas as pd
from utils.config_loader import load_config
from utils.db import get_all_records, insert_record

cfg = load_config()
currency = cfg["business"]["currency"]

st.title("📣 Ad & Promotion Tracker")

with st.expander("➕ Log New Campaign"):
    col1, col2 = st.columns(2)
    with col1:
        campaign_name = st.text_input("Campaign Name")
        platform = st.selectbox("Platform", ["WhatsApp Broadcast", "Instagram", "Facebook",
                                              "Google Ads", "JustDial", "IndiaMart",
                                              "Print / Pamphlet", "Word of Mouth", "Other"])
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
    with col2:
        budget = st.number_input(f"Budget ({currency})", min_value=0.0)
        spent = st.number_input(f"Amount Spent ({currency})", min_value=0.0)
        reach = st.number_input("Estimated Reach (people)", min_value=0)
        leads = st.number_input("Leads Generated", min_value=0)
        conversions = st.number_input("Conversions (sales closed)", min_value=0)
        revenue_from_campaign = st.number_input(f"Revenue Attributed ({currency})", min_value=0.0)

    notes = st.text_area("Notes")

    if st.button("Save Campaign", type="primary"):
        roi = ((revenue_from_campaign - spent) / spent * 100) if spent > 0 else 0
        insert_record("campaigns", {
            "name": campaign_name, "platform": platform,
            "start_date": str(start_date), "end_date": str(end_date),
            "budget": budget, "spent": spent, "reach": reach,
            "leads": leads, "conversions": conversions,
            "revenue": revenue_from_campaign, "roi_pct": round(roi, 1), "notes": notes,
        })
        st.success(f"Campaign saved! ROI: {roi:.1f}%")
        st.rerun()

# ── Summary metrics ──────────────────────────────────────────────────────────
st.divider()
campaigns = get_all_records("campaigns", order_col="start_date")

if campaigns:
    df = pd.DataFrame(campaigns)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Spent", f"{currency}{df['spent'].sum():,.0f}")
    col2.metric("Total Leads", int(df["leads"].sum()))
    col3.metric("Total Revenue", f"{currency}{df['revenue'].sum():,.0f}")
    avg_roi = df["roi_pct"].mean()
    col4.metric("Avg ROI", f"{avg_roi:.1f}%", delta="vs zero" if avg_roi > 0 else None)

    st.subheader("All Campaigns")
    st.dataframe(df[["name", "platform", "spent", "reach", "leads", "conversions", "revenue", "roi_pct"]],
                 use_container_width=True)
else:
    st.info("No campaigns logged yet.")
