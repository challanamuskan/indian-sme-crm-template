"""
pages/11_Business_Intelligence.py
Live charts: revenue trends, top products, customer spend, payment health.
"""

import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils.db import get_all_records
from utils.config_loader import load_config

cfg = load_config()
st.title("📊 Business Intelligence")
st.caption("Live insights from your sales, customers, and payments.")

try:
    sales     = get_all_records("sales")
    customers = get_all_records("customers")
    payments  = get_all_records("payments")
    campaigns = get_all_records("campaigns", order_col="start_date")
    products  = get_all_records("products")

    if not sales:
        st.info("No sales data yet. Add sales to see analytics.")
        st.stop()

    df_sales = pd.DataFrame(sales)
    df_sales["date"]  = pd.to_datetime(df_sales["date"])
    df_sales["total"] = pd.to_numeric(df_sales["total"], errors="coerce").fillna(0)
    df_sales["month"] = df_sales["date"].dt.strftime("%b %Y")

    # ── KPI row ───────────────────────────────────────────────────────────────
    total_rev  = df_sales["total"].sum()
    avg_order  = df_sales["total"].mean()
    top_month  = df_sales.groupby("month")["total"].sum().idxmax() if len(df_sales) > 1 else "—"

    df_pay = pd.DataFrame(payments)
    pending_amt = pd.to_numeric(df_pay[df_pay["status"] == "pending"]["amount"], errors="coerce").sum() if not df_pay.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue",    f"₹{total_rev:,.0f}")
    c2.metric("Avg Order Value",  f"₹{avg_order:,.0f}")
    c3.metric("Best Month",       top_month)
    c4.metric("Pending Payments", f"₹{pending_amt:,.0f}", delta="Needs collection", delta_color="inverse")

    st.divider()

    # ── Revenue trend ─────────────────────────────────────────────────────────
    st.subheader("Revenue Trend")
    monthly = df_sales.groupby("month")["total"].sum().reset_index()
    monthly.columns = ["Month", "Revenue"]
    st.bar_chart(monthly.set_index("Month"))

    col_a, col_b = st.columns(2)

    # ── Payment status pie ────────────────────────────────────────────────────
    with col_a:
        st.subheader("Payment Health")
        if not df_pay.empty:
            status_counts = df_pay["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            st.dataframe(status_counts, use_container_width=True, hide_index=True)
        else:
            st.info("No payment data yet.")

    # ── Low stock list ────────────────────────────────────────────────────────
    with col_b:
        st.subheader("Stock Health")
        threshold = cfg["display"]["low_stock_threshold"]
        df_prod = pd.DataFrame(products)
        if not df_prod.empty:
            df_prod["quantity"] = pd.to_numeric(df_prod["quantity"], errors="coerce").fillna(0)
            low = df_prod[df_prod["quantity"] < threshold][["name", "quantity", "unit"]]
            if not low.empty:
                st.warning(f"{len(low)} items below {threshold} units")
                st.dataframe(low.rename(columns={"name":"Product","quantity":"Stock","unit":"Unit"}),
                             use_container_width=True, hide_index=True)
            else:
                st.success("All products well-stocked!")

    # ── Campaign ROI ──────────────────────────────────────────────────────────
    st.subheader("Campaign ROI")
    if campaigns:
        df_camp = pd.DataFrame(campaigns)
        df_camp["spend"]  = pd.to_numeric(df_camp["spend"], errors="coerce").fillna(0)
        df_camp["budget"] = pd.to_numeric(df_camp["budget"], errors="coerce").fillna(1)
        df_camp["leads"]  = pd.to_numeric(df_camp["leads"], errors="coerce").fillna(0)
        df_camp["ROI %"]  = ((df_camp["budget"] - df_camp["spend"]) / df_camp["budget"] * 100).round(1)
        df_camp["Cost/Lead"] = (df_camp["spend"] / df_camp["leads"].replace(0, 1)).round(0)
        display = df_camp[["name", "channel", "budget", "spend", "leads", "ROI %", "Cost/Lead"]].copy()
        display.columns = ["Campaign", "Channel", "Budget ₹", "Spend ₹", "Leads", "ROI %", "₹/Lead"]
        st.dataframe(display, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Error loading data: {e}")
    st.caption("Ensure SUPABASE_URL and SUPABASE_KEY are set in Streamlit secrets.")
