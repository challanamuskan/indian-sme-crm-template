"""Indian SME CRM Template - Entry point"""

import streamlit as st
from utils.config_loader import load_config
from utils.auth import check_login, render_login_page

cfg = load_config()

st.set_page_config(
    page_title=cfg["business"]["name"],
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not check_login():
    render_login_page(cfg)
    st.stop()

with st.sidebar:
    st.title(cfg["business"]["name"])
    st.caption(cfg["business"].get("tagline", ""))
    st.divider()
    role = st.session_state.get("role", "staff")
    st.caption(f"Logged in as: **{st.session_state.get('username', '')}** ({role})")
    if st.button("Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ── Live KPIs from Supabase ──────────────────────────────────
st.title(f"Welcome to {cfg['business']['name']} CRM")

try:
    from supabase import create_client
    import datetime

    sb = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

    products  = sb.table("products").select("id,quantity", count="exact").execute()
    customers = sb.table("customers").select("id", count="exact").execute()
    payments_pending = sb.table("payments").select("id,amount").eq("status", "pending").execute()
    low_stock = [r for r in (products.data or []) if r.get("quantity", 99) < cfg["display"]["low_stock_threshold"]]

    # monthly revenue
    first_of_month = datetime.date.today().replace(day=1).isoformat()
    sales_month = sb.table("sales").select("total").gte("date", first_of_month).execute()
    monthly_rev = sum(float(r["total"] or 0) for r in (sales_month.data or []))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Stock Items", products.count or 0)
    col2.metric("👥 Customers", customers.count or 0)
    col3.metric("💰 Revenue This Month", f"₹{monthly_rev:,.0f}")
    col4.metric("⚠️ Low Stock", len(low_stock), delta=f"-{len(low_stock)} need reorder" if low_stock else None, delta_color="inverse")

    st.divider()

    # recent sales table
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Recent Sales")
        recent = sb.table("sales").select("id,date,total,status,customers(name)").order("date", desc=True).limit(5).execute()
        if recent.data:
            import pandas as pd
            df = pd.DataFrame([{
                "Customer": r.get("customers", {}).get("name", "—") if r.get("customers") else "—",
                "Amount": f"₹{float(r['total']):,.0f}",
                "Date": r["date"],
                "Status": r["status"].title(),
            } for r in recent.data])
            st.dataframe(df, use_container_width=True, hide_index=True)

    with col_b:
        st.subheader("Pending Payments")
        pending = sb.table("payments").select("amount,due_date,status,customers(name)").eq("status", "pending").order("due_date").limit(5).execute()
        if pending.data:
            import pandas as pd
            df2 = pd.DataFrame([{
                "Customer": r.get("customers", {}).get("name", "—") if r.get("customers") else "—",
                "Amount": f"₹{float(r['amount']):,.0f}",
                "Due": r.get("due_date", "—"),
            } for r in pending.data])
            st.dataframe(df2, use_container_width=True, hide_index=True)
        else:
            st.success("All payments up to date!")

except Exception as e:
    st.warning(f"Database not connected: {e}")
    st.info("Add SUPABASE_URL and SUPABASE_KEY in Streamlit secrets to see live data.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Stock Items", "—")
    col2.metric("👥 Customers", "—")
    col3.metric("💰 Revenue This Month", "₹ —")
    col4.metric("⚠️ Low Stock", "—")
