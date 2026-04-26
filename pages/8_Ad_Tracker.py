"""pages/8_Ad_Tracker.py — Track marketing campaigns, budget, ROI."""

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
        name       = st.text_input("Campaign Name")
        channel    = st.selectbox("Channel", ["WhatsApp Broadcast", "Instagram", "Facebook",
                                               "Google Ads", "JustDial", "IndiaMart",
                                               "Print / Pamphlet", "Word of Mouth", "Other"])
        start_date = st.date_input("Start Date")
        end_date   = st.date_input("End Date")
    with col2:
        budget      = st.number_input(f"Budget ({currency})", min_value=0.0)
        spend       = st.number_input(f"Amount Spent ({currency})", min_value=0.0)
        leads       = st.number_input("Leads Generated", min_value=0)
        conversions = st.number_input("Conversions", min_value=0)
    goal  = st.selectbox("Goal", ["Brand Awareness", "Lead Generation", "Sales", "Retention"])
    notes = st.text_area("Notes")

    if st.button("Save Campaign", type="primary"):
        insert_record("campaigns", {
            "name": name, "channel": channel,
            "start_date": str(start_date), "end_date": str(end_date),
            "budget": budget, "spend": spend,
            "leads": leads, "conversions": conversions,
            "goal": goal, "notes": notes,
        })
        st.success("Campaign saved!")
        st.rerun()

st.divider()
campaigns = get_all_records("campaigns", order_col="start_date")

if campaigns:
    df = pd.DataFrame(campaigns)
    # safe numeric conversion — handle missing columns gracefully
    for col in ["budget", "spend", "leads", "conversions"]:
        df[col] = pd.to_numeric(df.get(col, 0), errors="coerce").fillna(0)

    df["ROI %"]    = ((df["budget"] - df["spend"]) / df["budget"].replace(0,1) * 100).round(1)
    df["₹/Lead"]   = (df["spend"] / df["leads"].replace(0,1)).round(0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Spend",   f"{currency}{df['spend'].sum():,.0f}")
    c2.metric("Total Leads",   int(df["leads"].sum()))
    c3.metric("Conversions",   int(df["conversions"].sum()))
    c4.metric("Avg ROI",       f"{df['ROI %'].mean():.1f}%")

    st.subheader("All Campaigns")
    display_cols = [c for c in ["name", "channel", "budget", "spend", "leads", "conversions", "ROI %", "₹/Lead"] if c in df.columns or c in ["ROI %", "₹/Lead"]]
    st.dataframe(df[display_cols], use_container_width=True, hide_index=True)
else:
    st.info("No campaigns logged yet. Add your first campaign above.")
