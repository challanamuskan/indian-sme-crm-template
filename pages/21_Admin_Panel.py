"""pages/21_Admin_Panel.py — Admin-only: manage demo accounts, view usage"""

import streamlit as st

# Auth guard
if not st.session_state.get("authenticated", False):
    st.error("🔒 Please login first.")
    st.stop()

if st.session_state.get("role") != "admin":
    st.error("🔒 Admin access only.")
    st.stop()

from utils.auth import render_admin_temp_accounts

st.set_page_config(page_title="⚙️ Admin Panel", layout="wide")
st.title("⚙️ Admin Panel")
st.caption("Manage demo accounts · View usage · Reset limits")

render_admin_temp_accounts()

st.divider()
st.subheader("📋 How Demo Accounts Work")
st.markdown("""
- **7 client accounts**: `demo_client1` → `demo_client7`
- Each gets **5 logins** before expiring
- Usage is stored in Supabase `demo_usage` table (persists across restarts)
- **To share with a client**: give them the username + password you set in Streamlit secrets
- **Passwords** are set in Streamlit Cloud → App Settings → Secrets:
""")
st.code("""DEMO_CLIENT1_PASS = "your-chosen-password"
DEMO_CLIENT2_PASS = "another-password"
# ... up to DEMO_CLIENT7_PASS""", language="toml")

st.info("💡 After client finishes reviewing, use Reset above to restore their 5 uses for next session.")
