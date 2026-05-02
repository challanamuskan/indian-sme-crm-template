"""pages/16_Website_Manager.py — Website uptime, lead capture, analytics embed, SEO checklist."""

import streamlit as st
if not st.session_state.get("authenticated", False):
    st.error("\U0001f512 Please login first.")
    st.stop()

import streamlit as st
import urllib.request
from utils.config_loader import load_config

cfg = load_config()
st.title("🌐 Website Manager")
st.caption("Monitor your site, capture leads, track performance.")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "🔍 Uptime", "📥 Web Leads", "✅ SEO Checklist"])

# ── Tab 1: Analytics embed ────────────────────────────────────────────────────
with tab1:
    analytics_url = cfg["features"].get("website_analytics_url", "")
    if analytics_url:
        st.components.v1.iframe(analytics_url, height=620, scrolling=True)
    else:
        st.info("Add `website_analytics_url` in config.yaml to embed your analytics dashboard.")
        st.markdown("""
**Recommended free analytics tools:**
- [Plausible.io](https://plausible.io) — Privacy-first, simple embed
- [Umami](https://umami.is) — Self-hostable, free
- [Microsoft Clarity](https://clarity.microsoft.com) — Free heatmaps + session recordings
- [Google Analytics](https://analytics.google.com) — Most popular, free
        """)

# ── Tab 2: Uptime monitor ─────────────────────────────────────────────────────
with tab2:
    st.subheader("🔍 Site Status Check")
    urls_to_check = []
    if cfg["business"].get("website"):
        urls_to_check.append(cfg["business"]["website"])

    custom_url = st.text_input("Check any URL", placeholder="https://yoursite.com")
    if custom_url:
        urls_to_check.append(custom_url)

    if st.button("Check Now") and urls_to_check:
        for url in urls_to_check:
            try:
                code = urllib.request.urlopen(url, timeout=8).getcode()
                if code == 200:
                    st.success(f"✅ {url} — Online (HTTP {code})")
                else:
                    st.warning(f"⚠️ {url} — HTTP {code}")
            except Exception as e:
                st.error(f"❌ {url} — Unreachable")
    elif not urls_to_check:
        st.caption("Add `website` URL in config.yaml or enter one above.")

# ── Tab 3: Web leads ──────────────────────────────────────────────────────────
with tab3:
    st.subheader("📥 Website Contact Form Leads")
    st.info("Connect your website's contact form to capture leads here automatically.")

    # Demo data
    import pandas as pd
    from datetime import datetime, timedelta
    demo_leads = [
        {"Name":"Amit Kumar","Email":"amit@example.com","Phone":"+91987654321","Message":"Need 50 bearings bulk order","Date":str(datetime.now().date())},
        {"Name":"Sunita Sharma","Email":"sunita@example.com","Phone":"+91876543210","Message":"Looking for textile fabric samples","Date":str(datetime.now().date()-timedelta(days=1))},
    ]
    df_leads = pd.DataFrame(demo_leads)
    st.dataframe(df_leads, use_container_width=True, hide_index=True)
    st.caption("**To capture real leads:** add a webhook from your website form → POST to your Supabase `web_leads` table.")

    with st.expander("📋 Webhook Setup Guide"):
        st.code("""
# Your website form POSTs to this Supabase endpoint:
POST https://gkezuezfwygwkfukinhi.supabase.co/rest/v1/web_leads
Headers:
  apikey: YOUR_ANON_KEY
  Content-Type: application/json
Body:
  {"name": "...", "email": "...", "phone": "...", "message": "..."}
        """, language="bash")

# ── Tab 4: SEO checklist ──────────────────────────────────────────────────────
with tab4:
    st.subheader("✅ Basic SEO Checklist")
    checklist = {
        "Google Business Profile created and verified": False,
        "Business listed on JustDial": False,
        "Business listed on IndiaMart": False,
        "Google Search Console connected": False,
        "Website has title tags and meta descriptions": False,
        "Mobile-responsive website": False,
        "WhatsApp Business API linked to website": False,
        "Customer reviews on Google": False,
        "Product images optimised (< 200KB each)": False,
        "Contact page with phone + address + map embed": False,
    }
    score = 0
    for item in checklist:
        checked = st.checkbox(item, key=f"seo_{item}")
        if checked:
            score += 1
    st.progress(score / len(checklist))
    st.metric("SEO Score", f"{score}/{len(checklist)}", f"{int(score/len(checklist)*100)}%")
