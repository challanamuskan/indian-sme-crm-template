"""utils/auth_guard.py
Add this to the TOP of every page file (after imports) to block unauthenticated access.

Usage:
    from utils.auth_guard import require_login
    require_login()
"""
import streamlit as st


def require_login():
    """Stops page render if user not authenticated. Redirects to login."""
    if not st.session_state.get("authenticated", False):
        st.set_page_config(page_title="Login Required", page_icon="🔒")  # safe if not already set
        st.error("🔒 You must be logged in to view this page.")
        st.markdown("Please go back to the home page and log in.")
        st.stop()
