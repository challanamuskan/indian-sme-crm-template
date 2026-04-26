"""utils/auth.py — Session auth, role-based access, login UI"""

import hashlib
import streamlit as st


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def check_login() -> bool:
    return st.session_state.get("authenticated", False)


def require_admin():
    if st.session_state.get("role") != "admin":
        st.error("Admin access required.")
        st.stop()


def render_login_page(cfg: dict):
    st.title(f"🔐 {cfg['business']['name']}")
    st.subheader("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        # ── Replace with Supabase user lookup in production ──
        # This stub checks against Streamlit secrets
        import streamlit as st_inner
        secrets = st_inner.secrets if hasattr(st_inner, "secrets") else {}
        users = secrets.get("users", {})

        if username in users and users[username]["password_hash"] == _hash(password):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username].get("role", "staff")
            st.rerun()
        else:
            st.error("Invalid credentials.")
