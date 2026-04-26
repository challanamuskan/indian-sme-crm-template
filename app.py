"""
Indian SME CRM Template
Entry point — loads config, handles login, renders sidebar nav.
"""

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

# ── Auth gate ──────────────────────────────────────────────
if not check_login():
    render_login_page(cfg)
    st.stop()

# ── Sidebar ────────────────────────────────────────────────
with st.sidebar:
    logo_url = cfg["business"].get("logo_url", "")
    if logo_url:
        st.image(logo_url, width=120)
    st.title(cfg["business"]["name"])
    st.caption(cfg["business"]["tagline"])
    st.divider()

    role = st.session_state.get("role", "staff")
    st.caption(f"Logged in as: **{st.session_state.get('username', '')}** ({role})")
    if st.button("Logout", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# ── Home dashboard ─────────────────────────────────────────
st.title(f"Welcome to {cfg['business']['name']} CRM")
st.markdown("Use the **sidebar** to navigate between modules.")

col1, col2, col3, col4 = st.columns(4)
# KPI cards — wired to live Supabase counts in production
with col1:
    st.metric("📦 Stock Items", "—", help="Live from Stock Manager")
with col2:
    st.metric("👥 Customers", "—", help="Live from Customers")
with col3:
    st.metric("💰 Sales This Month", "₹ —", help="Live from Sales")
with col4:
    st.metric("⚠️ Low Stock Alerts", "—", help="Items below threshold")

st.info("🚀 Configure your business in `config.yaml` before first use. See [docs/deploy.md](docs/deploy.md).")
