"""utils/auth.py - Session auth, role-based access, login UI"""

import streamlit as st

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

def check_login() -> bool:
    return st.session_state.get("authenticated", False)

def render_login_page(cfg: dict = None):
    biz_name = (cfg or {}).get("business", {}).get("name", "SME CRM")
    st.markdown(f"## {biz_name}")
    st.markdown("#### Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)
    if submitted:
        users = _get_users()
        user = users.get(username)
        if user and user["password"] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user["role"]
            st.rerun()
        else:
            st.error("Invalid credentials.")
            st.caption("Demo: username **admin** / password **demo123**")

def require_admin():
    if st.session_state.get("role") != "admin":
        st.error("Admin access required.")
        st.stop()

def get_role() -> str:
    return st.session_state.get("role", "viewer")
