"""pages/14_Stock_Tracker.py — Live stock, reorder, supplier tracking."""

import streamlit as st
import pandas as pd
from utils.config_loader import load_config
from utils.db import get_all_records, insert_record

cfg = load_config()
currency = cfg["business"]["currency"]
threshold = cfg["display"]["low_stock_threshold"]

st.title("📦 Stock Tracker")

try:
    products = get_all_records("products", order_col="name")
    df = pd.DataFrame(products) if products else pd.DataFrame()

    if not df.empty:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
        df["price"]    = pd.to_numeric(df["price"],    errors="coerce").fillna(0)
        df["stock_value"] = df["quantity"] * df["price"]

        # ── KPIs ──────────────────────────────────────────────────────────────
        low_stock = df[df["quantity"] < threshold]
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Products",  len(df))
        c2.metric("Low Stock Items", len(low_stock), delta=f"{len(low_stock)} need reorder" if len(low_stock) else None, delta_color="inverse")
        c3.metric("Total Stock Value", f"{currency}{df['stock_value'].sum():,.0f}")
        c4.metric("Out of Stock",    int((df["quantity"] == 0).sum()))

        # ── Low stock alert ───────────────────────────────────────────────────
        if not low_stock.empty:
            st.error(f"⚠️ {len(low_stock)} item(s) below {threshold} units")
            alert_df = low_stock[["name","category","quantity","unit","supplier"]].copy()
            alert_df.columns = ["Product","Category","Stock","Unit","Supplier"]
            st.dataframe(alert_df, use_container_width=True, hide_index=True)

        st.divider()

        # ── Category filter ───────────────────────────────────────────────────
        categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
        col_f, col_s = st.columns([2,1])
        cat_filter  = col_f.selectbox("Filter by category", categories)
        search      = col_s.text_input("Search product")

        view = df.copy()
        if cat_filter != "All":
            view = view[view["category"] == cat_filter]
        if search:
            view = view[view["name"].str.contains(search, case=False, na=False)]

        view["Status"] = view["quantity"].apply(
            lambda q: "🔴 Out" if q == 0 else ("🟡 Low" if q < threshold else "🟢 OK")
        )
        display = view[["name","category","quantity","unit","price","stock_value","supplier","Status"]].copy()
        display.columns = ["Product","Category","Qty","Unit","Price ₹","Value ₹","Supplier","Status"]
        st.dataframe(display, use_container_width=True, hide_index=True)

        # ── Value by category chart ───────────────────────────────────────────
        st.subheader("Stock Value by Category")
        cat_val = df.groupby("category")["stock_value"].sum().reset_index()
        cat_val.columns = ["Category","Value"]
        st.bar_chart(cat_val.set_index("Category"))

    else:
        st.info("No products yet.")

    # ── Add product ───────────────────────────────────────────────────────────
    with st.expander("➕ Add New Product"):
        c1, c2 = st.columns(2)
        name     = c1.text_input("Product Name")
        category = c2.text_input("Category")
        qty      = c1.number_input("Opening Stock", min_value=0)
        unit     = c2.text_input("Unit", value="pcs")
        price    = c1.number_input(f"Price ({currency})", min_value=0.0)
        hsn      = c2.text_input("HSN Code")
        supplier = st.text_input("Supplier")
        if st.button("Add Product", type="primary"):
            insert_record("products", {"name":name,"category":category,"quantity":qty,
                                        "unit":unit,"price":price,"hsn_code":hsn,"supplier":supplier})
            st.success(f"✅ {name} added!")
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
