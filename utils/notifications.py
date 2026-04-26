"""
utils/notifications.py — Gmail + WhatsApp notifications
Toggle via config.yaml: features.gmail_enabled / features.whatsapp_enabled
"""

from __future__ import annotations
import urllib.parse
from utils.config_loader import load_config

cfg = load_config()


# ── WhatsApp ──────────────────────────────────────────────────────────────────

def whatsapp_link(phone: str, message: str) -> str:
    """
    Returns a wa.me click-to-open link.
    Use with st.link_button("Send via WhatsApp", whatsapp_link(...))
    phone: Indian mobile, e.g. "9876543210" or "+919876543210"
    """
    if not cfg["features"].get("whatsapp_enabled"):
        return ""
    clean = phone.replace("+", "").replace(" ", "").replace("-", "")
    if not clean.startswith("91"):
        clean = "91" + clean
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{clean}?text={encoded}"


def payment_reminder_whatsapp(customer_name: str, phone: str, amount: float, due_date: str) -> str:
    biz = cfg["business"]["name"]
    currency = cfg["business"]["currency"]
    msg = (
        f"Dear {customer_name},\n\n"
        f"This is a friendly reminder from *{biz}*.\n"
        f"Payment of *{currency}{amount:,.0f}* is due on *{due_date}*.\n\n"
        f"Please arrange payment at your earliest convenience.\n\nThank you 🙏"
    )
    return whatsapp_link(phone, msg)


# ── Gmail ─────────────────────────────────────────────────────────────────────

def send_payment_reminder_email(customer_email: str, customer_name: str,
                                 amount: float, due_date: str) -> bool:
    """
    Sends a payment reminder via Gmail API.
    Requires: Gmail API credentials in Streamlit secrets.
    Returns True on success, False if disabled or error.
    """
    if not cfg["features"].get("gmail_enabled"):
        return False

    # ── Gmail API logic lives here in production ──
    # Kept as interface stub in template — see docs/gmail_setup.md
    raise NotImplementedError(
        "Gmail integration requires credentials setup. "
        "Follow docs/gmail_setup.md then implement send logic here."
    )
