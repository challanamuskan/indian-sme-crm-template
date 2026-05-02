"""utils/auth.py — Session auth, role-based access, login UI, temp demo accounts"""

import streamlit as st
import json
from datetime import datetime

# ─── Temp Demo Accounts (7 accounts × 5 uses each) ────────────
# Each account gets 5 login attempts. Usage tracked in session state.
# In production, wire usage counts to Supabase for persistence.
TEMP_ACCOUNTS = {
    "demo_client1": {"password": "client1pass", "role": "viewer", "label": "Client Preview 1", "max_uses": 5},
    "demo_client2": {"password": "client2pass", "role": "viewer", "label": "Client Preview 2", "max_uses": 5},
    "demo_client3": {"password": "client3pass", "role": "viewer", "label": "Client Preview 3", "max_uses": 5},
    "demo_client4": {"password": "client4pass", "role": "viewer", "label": "Client Preview 4", "max_uses": 5},
    "demo_client5": {"password": "client5pass", "role": "viewer", "label": "Client Preview 5", "max_uses": 5},
    "demo_client6": {"password": "client6pass", "role": "viewer", "label": "Client Preview 6", "max_uses": 5},
    "demo_client7": {"password": "client7pass", "role": "viewer", "label": "Client Preview 7", "max_uses": 5},
}

_DEFAULT_USERS = {
    "admin": {"password": "demo123", "role": "admin"},
    "staff": {"password": "staff123", "role": "staff"},
}


def _get_users() -> dict:
    try:
        username = st.secrets.get("ADMIN_USERNAME", "admin")
        password = st.secrets.get("ADMIN_PASSWORD", "demo123")
        users = {username: {"password": password, "role": "admin"}}
        if st.secrets.get("STAFF_USERNAME"):
            users[st.secrets["STAFF_USERNAME"]] = {
                "password": st.secrets.get("STAFF_PASSWORD", "staff123"),
                "role": "staff",
            }
        return users
    except Exception:
        return _DEFAULT_USERS


def _get_usage_counts() -> dict:
    """Get temp account usage counts from session state (resets on app restart).
    Wire to Supabase for persistence across sessions."""
    if "_temp_usage" not in st.session_state:
        st.session_state._temp_usage = {k: 0 for k in TEMP_ACCOUNTS}
    return st.session_state._temp_usage


def _increment_usage(username: str):
    counts = _get_usage_counts()
    counts[username] = counts.get(username, 0) + 1
    st.session_state._temp_usage = counts


def _uses_remaining(username: str) -> int:
    if username not in TEMP_ACCOUNTS:
        return 999
    counts = _get_usage_counts()
    used = counts.get(username, 0)
    return max(0, TEMP_ACCOUNTS[username]["max_uses"] - used)


def check_login() -> bool:
    return st.session_state.get("authenticated", False)


def render_login_page(cfg: dict = None):
    biz_name = (cfg or {}).get("business", {}).get("name", "SME CRM")

    st.markdown(f"## 🏪 {biz_name}")

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("#### Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login", use_container_width=True)

        if submitted:
            # 1. Check permanent users first
            users = _get_users()
            user = users.get(username)
            if user and user["password"] == password:
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user["role"]
                st.session_state["logged_in"] = True
                st.rerun()
                return

            # 2. Check temp accounts
            if username in TEMP_ACCOUNTS:
                temp = TEMP_ACCOUNTS[username]
                if temp["password"] == password:
                    remaining = _uses_remaining(username)
                    if remaining <= 0:
                        st.error(f"❌ Demo account **{username}** has expired (5/5 uses used).")
                        st.info("Contact Muskan Challana to request a new demo access.")
                        return
                    _increment_usage(username)
                    remaining_after = _uses_remaining(username)
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = "viewer"
                    st.session_state["logged_in"] = True
                    st.session_state["is_demo"] = True
                    st.session_state["demo_uses_remaining"] = remaining_after
                    st.rerun()
                    return

            st.error("❌ Invalid credentials.")
            st.caption("Demo: username **admin** / password **demo123**")

    with col_side:
        st.markdown("#### 🔑 Demo Access")
        st.caption("7 client preview accounts available. Each gets 5 logins.")
        st.markdown("""
| Account | Password |
|---------|----------|
| `demo_client1` | `client1pass` |
| `demo_client2` | `client2pass` |
| `demo_client3` | `client3pass` |
| `demo_client4` | `client4pass` |
| `demo_client5` | `client5pass` |
| `demo_client6` | `client6pass` |
| `demo_client7` | `client7pass` |
""")
        st.caption("⚡ Admin: `admin` / `demo123`")

        # Show usage status
        counts = _get_usage_counts()
        active = sum(1 for k in TEMP_ACCOUNTS if counts.get(k, 0) < TEMP_ACCOUNTS[k]["max_uses"])
        st.metric("Active demo accounts", f"{active}/7")


def render_demo_banner():
    """Call in app.py sidebar to show demo usage warning."""
    if st.session_state.get("is_demo"):
        remaining = st.session_state.get("demo_uses_remaining", 0)
        if remaining <= 1:
            st.sidebar.warning(f"⚠️ Demo account: **{remaining} login(s) left**")
        else:
            st.sidebar.info(f"👁️ Demo preview · {remaining} logins remaining")


def render_admin_temp_accounts():
    """Admin panel widget to view/reset temp account usage. Call from an admin-only page."""
    st.subheader("🔑 Temp Demo Account Manager")
    counts = _get_usage_counts()
    rows = []
    for acct, cfg in TEMP_ACCOUNTS.items():
        used = counts.get(acct, 0)
        remaining = max(0, cfg["max_uses"] - used)
        rows.append({
            "Account": acct,
            "Label": cfg["label"],
            "Used": used,
            "Max": cfg["max_uses"],
            "Remaining": remaining,
            "Status": "✅ Active" if remaining > 0 else "❌ Expired"
        })
    import pandas as pd
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)

    if st.button("🔄 Reset All Demo Accounts", type="secondary"):
        st.session_state._temp_usage = {k: 0 for k in TEMP_ACCOUNTS}
        st.success("✅ All 7 demo accounts reset to 5 uses each!")
        st.rerun()

    acct_to_reset = st.selectbox("Reset single account", ["— select —"] + list(TEMP_ACCOUNTS.keys()))
    if acct_to_reset != "— select —" and st.button("Reset Selected Account"):
        st.session_state._temp_usage[acct_to_reset] = 0
        st.success(f"✅ {acct_to_reset} reset!")
        st.rerun()


def require_admin():
    if st.session_state.get("role") != "admin":
        st.error("Admin access required.")
        st.stop()


def get_role() -> str:
    return st.session_state.get("role", "viewer")
