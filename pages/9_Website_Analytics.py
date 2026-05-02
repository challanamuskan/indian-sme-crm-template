"""
pages/9_Website_Analytics.py
Embed your website analytics dashboard (Plausible / Umami / GA / custom).
Also shows website health status and uptime.
"""

import streamlit as st
if not st.session_state.get("authenticated", False):
    st.error("\U0001f512 Please login first.")
    st.stop()

import streamlit as st
from utils.config_loader import load_config

cfg = load_config()
analytics_url = cfg["features"].get("website_analytics_url", "")

st.title("🌐 Website Analytics")

if not analytics_url:
    st.warning("No analytics URL configured. Set `features.website_analytics_url` in `config.yaml`.")
    st.markdown("""
**Supported analytics platforms:**
- [Plausible.io](https://plausible.io) — privacy-friendly, easy embed ✅
- [Umami](https://umami.is) — open source, self-hostable ✅
- [Google Analytics](https://analytics.google.com) ✅
- Any iframe-embeddable dashboard

**Config example:**
```yaml
features:
  website_analytics_url: "https://plausible.io/share/yourdomain.com?auth=xxx"
```
""")
else:
    st.components.v1.iframe(analytics_url, height=700, scrolling=True)

# ── Quick metrics log (manual entry if no analytics embed) ───────────────────
st.divider()
st.subheader("📝 Manual Traffic Log")
st.caption("Log weekly website traffic manually if you don't have an analytics tool yet.")

col1, col2, col3 = st.columns(3)
with col1: visitors = st.number_input("Weekly Visitors", min_value=0)
with col2: leads = st.number_input("Leads from Website", min_value=0)
with col3: source = st.selectbox("Top Traffic Source", ["Direct", "Google", "Instagram", "Facebook", "WhatsApp", "Other"])

if st.button("Log This Week"):
    from utils.db import insert_record
    from datetime import date
    insert_record("website_log", {
        "week_of": str(date.today()),
        "visitors": visitors, "leads": leads, "top_source": source
    })
    st.success("Logged!")
