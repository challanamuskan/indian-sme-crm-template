"""utils/auth.py — Session auth, role-based access, login UI, temp demo accounts"""

import streamlit as st

_TEMP_ACCOUNT_KEYS = [f"demo_client{i}" for i in range(1, 8)]
_TEMP_MAX_USES = 5


def _get_temp_password(username: str) -> str:
    key = username.upper() + "_PASS"
    try:
        return st.secrets.get(key, f"{username}pass")
    except Exception:
        return f"{username}pass"


def _build_temp_accounts() -> dict:
    return {
        u: {"password": _get_temp_password(u), "role": "viewer",
            "label": f"Client Preview {i+1}", "max_uses": _TEMP_MAX_USES}
        for i, u in enumerate(_TEMP_ACCOUNT_KEYS)
    }


def _get_permanent_users() -> dict:
    def s(key, default):
        try:
            return st.secrets.get(key, default)
        except Exception:
            return default

    users = {}
    # Admin
    users[s("ADMIN_USERNAME", "admin")] = {
        "password": s("ADMIN_PASSWORD", "demo123"), "role": "admin"
    }
    # Staff — always registered so staff login works without secrets configured
    users[s("STAFF_USERNAME", "staff")] = {
        "password": s("STAFF_PASSWORD", "staff123"), "role": "staff"
    }
    return users


def _get_usage_counts() -> dict:
    if "_temp_usage" not in st.session_state:
        st.session_state._temp_usage = {k: 0 for k in _TEMP_ACCOUNT_KEYS}
    return st.session_state._temp_usage


def _increment_usage(username: str):
    counts = _get_usage_counts()
    counts[username] = counts.get(username, 0) + 1
    st.session_state._temp_usage = counts


def _uses_remaining(username: str) -> int:
    return max(0, _TEMP_MAX_USES - _get_usage_counts().get(username, 0))


def _do_login(username, role, is_demo=False, uses_remaining=0):
    st.session_state.update({
        "authenticated": True, "logged_in": True,
        "username": username, "role": role,
    })
    if is_demo:
        st.session_state["is_demo"] = True
        st.session_state["demo_uses_remaining"] = uses_remaining


def check_login() -> bool:
    return st.session_state.get("authenticated", False)


def render_login_page(cfg: dict = None):
    biz_name = (cfg or {}).get("business", {}).get("name", "SME CRM")
    st.markdown(f"## 🏪 {biz_name}")
    st.markdown("#### Login to continue")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        # Check permanent users (admin + staff)
        perm = _get_permanent_users()
        if username in perm and perm[username]["password"] == password:
            _do_login(username, perm[username]["role"])
            st.rerun()
            return

        # Check temp demo accounts
        if username in _TEMP_ACCOUNT_KEYS:
            temp = _build_temp_accounts()
            if temp[username]["password"] == password:
                remaining = _uses_remaining(username)
                if remaining <= 0:
                    st.error(f"❌ Demo account **{username}** expired — all {_TEMP_MAX_USES} uses used.")
                    st.info("Contact admin for a fresh demo link.")
                    return
                _increment_usage(username)
                _do_login(username, "viewer", is_demo=True,
                          uses_remaining=_uses_remaining(username))
                st.rerun()
                return

        st.error("❌ Invalid username or password.")

    st.caption("Contact the admin for login credentials.")


def render_admin_temp_accounts():
    st.subheader("🔑 Demo Account Manager")
    counts = _get_usage_counts()
    rows = [{"Account": u, "Used": f"{counts.get(u,0)}/{_TEMP_MAX_USES}",
             "Remaining": _uses_remaining(u),
             "Status": "✅ Active" if _uses_remaining(u) > 0 else "❌ Expired"}
            for u in _TEMP_ACCOUNT_KEYS]
    import pandas as pd
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    col1, col2 = st.columns(2)
    if col1.button("🔄 Reset ALL", type="secondary"):
        st.session_state._temp_usage = {k: 0 for k in _TEMP_ACCOUNT_KEYS}
        st.success("✅ All 7 accounts reset!")
        st.rerun()
    acct = col2.selectbox("Reset one", ["— select —"] + _TEMP_ACCOUNT_KEYS)
    if acct != "— select —" and st.button("Reset Selected"):
        st.session_state._temp_usage[acct] = 0
        st.success(f"✅ {acct} reset!")
        st.rerun()

    st.divider()
    st.caption("Set custom passwords in Streamlit secrets:")
    st.code("DEMO_CLIENT1_PASS = \"your-pass\"\nDEMO_CLIENT2_PASS = \"pass2\"\n# ... up to DEMO_CLIENT7_PASS", language="toml")


def require_admin():
    if st.session_state.get("role") != "admin":
        st.error("Admin access required.")
        st.stop()


def get_role() -> str:
    return st.session_state.get("role", "viewer")
