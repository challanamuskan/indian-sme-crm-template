"""utils/auth.py — Auth + temp demo accounts with Supabase-persisted usage counts"""

import streamlit as st

_TEMP_KEYS = [f"demo_client{i}" for i in range(1, 8)]
_MAX_USES = 5


# ── Helpers ───────────────────────────────────────────────────
def _secret(key, default=""):
    try:
        return st.secrets.get(key, default)
    except Exception:
        return default


def _get_permanent_users() -> dict:
    users = {}
    users[_secret("ADMIN_USERNAME", "admin")] = {
        "password": _secret("ADMIN_PASSWORD", "demo123"), "role": "admin"
    }
    users[_secret("STAFF_USERNAME", "staff")] = {
        "password": _secret("STAFF_PASSWORD", "staff123"), "role": "staff"
    }
    return users


def _temp_password(username: str) -> str:
    return _secret(username.upper() + "_PASS", f"{username}pass")


# ── Supabase usage persistence ────────────────────────────────
def _get_sb():
    try:
        from supabase import create_client
        return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    except Exception:
        return None


def _load_usage() -> dict:
    """Load usage counts from Supabase demo_usage table. Falls back to session_state."""
    sb = _get_sb()
    if sb:
        try:
            rows = sb.table("demo_usage").select("username,count").execute().data or []
            return {r["username"]: r["count"] for r in rows}
        except Exception:
            pass
    # Fallback: session_state (resets on restart — acceptable for local dev)
    if "_temp_usage" not in st.session_state:
        st.session_state._temp_usage = {k: 0 for k in _TEMP_KEYS}
    return st.session_state._temp_usage


def _save_usage(username: str, count: int):
    sb = _get_sb()
    if sb:
        try:
            sb.table("demo_usage").upsert(
                {"username": username, "count": count},
                on_conflict="username"
            ).execute()
            return
        except Exception:
            pass
    # Fallback to session_state
    if "_temp_usage" not in st.session_state:
        st.session_state._temp_usage = {}
    st.session_state._temp_usage[username] = count


def _uses_remaining(username: str) -> int:
    usage = _load_usage()
    return max(0, _MAX_USES - usage.get(username, 0))


def _increment_usage(username: str):
    usage = _load_usage()
    new_count = usage.get(username, 0) + 1
    _save_usage(username, new_count)


def reset_usage(username: str = None):
    """Reset one or all temp accounts. Called from admin page."""
    targets = [username] if username else _TEMP_KEYS
    for u in targets:
        _save_usage(u, 0)
    # Also clear session_state fallback
    if "_temp_usage" in st.session_state:
        for u in targets:
            st.session_state._temp_usage[u] = 0


# ── Core auth ─────────────────────────────────────────────────
def check_login() -> bool:
    return st.session_state.get("authenticated", False)


def _do_login(username, role, is_demo=False, uses_left=0):
    st.session_state.update({
        "authenticated": True, "logged_in": True,
        "username": username, "role": role,
        "is_demo": is_demo,
        "demo_uses_remaining": uses_left,
    })


def render_login_page(cfg: dict = None):
    biz_name = (cfg or {}).get("business", {}).get("name", "SME CRM")
    st.markdown(f"## 🏪 {biz_name}")

    col_form, col_info = st.columns([3, 2])

    with col_form:
        st.markdown("#### Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("🔑 Login", use_container_width=True)

        if submitted:
            username = username.strip()

            # 1. Permanent users (admin / staff)
            perm = _get_permanent_users()
            if username in perm:
                if perm[username]["password"] == password:
                    _do_login(username, perm[username]["role"])
                    st.rerun()
                    return
                else:
                    st.error("❌ Wrong password.")
                    return

            # 2. Temp demo accounts
            if username in _TEMP_KEYS:
                if _temp_password(username) == password:
                    remaining = _uses_remaining(username)
                    if remaining <= 0:
                        st.error(f"❌ This demo account has expired. Contact admin.")
                        return
                    _increment_usage(username)
                    _do_login(username, "viewer", is_demo=True,
                              uses_left=_uses_remaining(username))
                    st.rerun()
                    return
                else:
                    st.error("❌ Wrong password.")
                    return

            st.error("❌ Username not found.")

    with col_info:
        st.markdown("#### Access")
        st.info("Contact the admin to receive your login credentials.")
        st.caption("🔒 All pages are protected. Login required.")


def require_admin():
    if st.session_state.get("role") != "admin":
        st.error("🔒 Admin access required.")
        st.stop()


def get_role() -> str:
    return st.session_state.get("role", "viewer")


# ── Admin panel widget ─────────────────────────────────────────
def render_admin_temp_accounts():
    """Embed in any admin-only page to manage demo account usage."""
    import pandas as pd
    st.subheader("🔑 Demo Account Manager")

    usage = _load_usage()
    rows = []
    for u in _TEMP_KEYS:
        used = usage.get(u, 0)
        rem = max(0, _MAX_USES - used)
        rows.append({
            "Account": u,
            "Used": f"{used} / {_MAX_USES}",
            "Remaining": rem,
            "Status": "✅ Active" if rem > 0 else "❌ Expired"
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()
    col1, col2 = st.columns(2)

    if col1.button("🔄 Reset ALL accounts", type="primary", use_container_width=True):
        reset_usage()
        st.success("✅ All 7 demo accounts reset to 5 uses!")
        st.rerun()

    sel = col2.selectbox("Reset single account", ["— pick one —"] + _TEMP_KEYS)
    if sel != "— pick one —":
        if st.button(f"Reset {sel}", use_container_width=True):
            reset_usage(sel)
            st.success(f"✅ {sel} reset to 5 uses!")
            st.rerun()
