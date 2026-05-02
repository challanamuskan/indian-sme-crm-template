import streamlit as st
if not st.session_state.get("authenticated", False):
    st.error("\U0001f512 Please login first.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta

st.set_page_config(page_title="📣 Marketing & Growth", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login first")
    st.stop()

def init_marketing():
    if "campaigns" not in st.session_state:
        st.session_state.campaigns = pd.DataFrame([
            {"Campaign": "Eid Sale WhatsApp Blast", "Channel": "WhatsApp", "Status": "Active",
             "Budget": 5000.0, "Spent": 2200.0, "Leads": 45, "Conversions": 8,
             "Start": "2026-04-01", "End": "2026-04-30"},
            {"Campaign": "Google Ads – Textile Parts", "Channel": "Google Ads", "Status": "Active",
             "Budget": 15000.0, "Spent": 8700.0, "Leads": 120, "Conversions": 22,
             "Start": "2026-04-01", "End": "2026-05-31"},
            {"Campaign": "LinkedIn Export Outreach", "Channel": "LinkedIn", "Status": "Completed",
             "Budget": 3000.0, "Spent": 3000.0, "Leads": 18, "Conversions": 3,
             "Start": "2026-03-01", "End": "2026-03-31"},
        ])
    if "growth_metrics" not in st.session_state:
        st.session_state.growth_metrics = pd.DataFrame([
            {"Month": "Jan 2026", "Revenue": 280000, "New_Customers": 4, "Repeat_Customers": 12,
             "Website_Visits": 850, "WhatsApp_Inquiries": 35, "Conversion_Rate": 18.5},
            {"Month": "Feb 2026", "Revenue": 310000, "New_Customers": 6, "Repeat_Customers": 14,
             "Website_Visits": 920, "WhatsApp_Inquiries": 42, "Conversion_Rate": 19.2},
            {"Month": "Mar 2026", "Revenue": 295000, "New_Customers": 5, "Repeat_Customers": 15,
             "Website_Visits": 1050, "WhatsApp_Inquiries": 55, "Conversion_Rate": 20.0},
            {"Month": "Apr 2026", "Revenue": 362000, "New_Customers": 9, "Repeat_Customers": 17,
             "Website_Visits": 1340, "WhatsApp_Inquiries": 68, "Conversion_Rate": 22.5},
        ])
    if "content_calendar" not in st.session_state:
        st.session_state.content_calendar = pd.DataFrame([
            {"Date": "2026-05-05", "Platform": "Instagram", "Type": "Product Post",
             "Caption": "Our premium textile parts ready for export 🌍", "Status": "Scheduled"},
            {"Date": "2026-05-07", "Platform": "WhatsApp", "Type": "Promo Broadcast",
             "Caption": "Eid discount – 10% on all orders above ₹50k", "Status": "Draft"},
            {"Date": "2026-05-10", "Platform": "LinkedIn", "Type": "Industry Article",
             "Caption": "How Indian SMEs are winning global textile contracts", "Status": "Draft"},
        ])

init_marketing()

st.title("📣 Marketing & Growth")
st.caption("Campaign tracking · Growth metrics · Content calendar · ROI analysis")

tabs = st.tabs([
    "📊 Growth Dashboard",
    "🎯 Campaigns",
    "📅 Content Calendar",
    "📧 Message Templates",
    "🏆 Customer Segments",
])

# ── TAB 1: GROWTH DASHBOARD ────────────────────────────────────
with tabs[0]:
    gm = st.session_state.growth_metrics
    latest = gm.iloc[-1]
    prev = gm.iloc[-2] if len(gm) > 1 else latest

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue (Latest)", f"₹{latest['Revenue']:,.0f}",
                delta=f"₹{latest['Revenue']-prev['Revenue']:,.0f}")
    col2.metric("New Customers", int(latest["New_Customers"]),
                delta=int(latest["New_Customers"] - prev["New_Customers"]))
    col3.metric("WA Inquiries", int(latest["WhatsApp_Inquiries"]),
                delta=int(latest["WhatsApp_Inquiries"] - prev["WhatsApp_Inquiries"]))
    col4.metric("Conversion Rate", f"{latest['Conversion_Rate']}%",
                delta=f"{latest['Conversion_Rate'] - prev['Conversion_Rate']:.1f}%")

    col_l, col_r = st.columns(2)
    with col_l:
        fig = px.area(gm, x="Month", y="Revenue", title="Monthly Revenue",
                      color_discrete_sequence=["#FF6B35"])
        fig.update_traces(fill="tozeroy", fillcolor="rgba(255,107,53,0.15)")
        st.plotly_chart(fig, use_container_width=True)
    with col_r:
        fig2 = px.bar(gm, x="Month", y=["New_Customers", "Repeat_Customers"],
                      title="New vs Repeat Customers", barmode="group",
                      color_discrete_sequence=["#2ECC71", "#3498DB"])
        st.plotly_chart(fig2, use_container_width=True)

    col_l2, col_r2 = st.columns(2)
    with col_l2:
        fig3 = px.line(gm, x="Month", y="Website_Visits", title="Website Traffic",
                       markers=True, color_discrete_sequence=["#9B59B6"])
        st.plotly_chart(fig3, use_container_width=True)
    with col_r2:
        fig4 = px.line(gm, x="Month", y="Conversion_Rate", title="Conversion Rate %",
                       markers=True, color_discrete_sequence=["#F39C12"])
        fig4.add_hline(y=20, line_dash="dash", line_color="gray", annotation_text="Target 20%")
        st.plotly_chart(fig4, use_container_width=True)

    with st.expander("➕ Add Monthly Growth Data"):
        g1, g2, g3 = st.columns(3)
        m_in = g1.text_input("Month (e.g. May 2026)")
        rev_in = g1.number_input("Revenue (₹)", min_value=0.0, step=1000.0)
        nc = g2.number_input("New Customers", min_value=0, step=1)
        rc = g2.number_input("Repeat Customers", min_value=0, step=1)
        wv = g3.number_input("Website Visits", min_value=0, step=10)
        wa = g3.number_input("WhatsApp Inquiries", min_value=0, step=1)
        cr = g3.number_input("Conversion Rate (%)", min_value=0.0, max_value=100.0, step=0.5)
        if st.button("💾 Save Growth Data", type="primary"):
            new_row = pd.DataFrame([{"Month": m_in, "Revenue": rev_in, "New_Customers": nc,
                                      "Repeat_Customers": rc, "Website_Visits": wv,
                                      "WhatsApp_Inquiries": wa, "Conversion_Rate": cr}])
            st.session_state.growth_metrics = pd.concat(
                [st.session_state.growth_metrics, new_row], ignore_index=True)
            st.success("✅ Saved!")
            st.rerun()

# ── TAB 2: CAMPAIGNS ───────────────────────────────────────────
with tabs[1]:
    st.subheader("🎯 Active Campaigns")
    df_c = st.session_state.campaigns.copy()
    df_c["ROI%"] = ((df_c["Budget"] - df_c["Spent"]) / df_c["Budget"].replace(0, 1) * 100).round(1)
    df_c["₹/Lead"] = (df_c["Spent"] / df_c["Leads"].replace(0, 1)).round(0)
    df_c["Conv%"] = (df_c["Conversions"] / df_c["Leads"].replace(0, 1) * 100).round(1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Budget", f"₹{df_c['Budget'].sum():,.0f}")
    col2.metric("Total Spent", f"₹{df_c['Spent'].sum():,.0f}")
    col3.metric("Total Leads", int(df_c["Leads"].sum()))
    col4.metric("Total Conversions", int(df_c["Conversions"].sum()))

    st.dataframe(df_c, use_container_width=True, hide_index=True)

    col_l, col_r = st.columns(2)
    with col_l:
        fig_ch = px.bar(df_c, x="Channel", y="Leads", color="Status",
                        title="Leads by Channel")
        st.plotly_chart(fig_ch, use_container_width=True)
    with col_r:
        fig_roi = px.bar(df_c, x="Campaign", y="ROI%", title="ROI % by Campaign",
                         color="ROI%", color_continuous_scale="RdYlGn")
        st.plotly_chart(fig_roi, use_container_width=True)

    with st.expander("➕ Add Campaign"):
        c1, c2, c3 = st.columns(3)
        camp_name = c1.text_input("Campaign Name")
        channel = c1.selectbox("Channel", ["WhatsApp", "Instagram", "Google Ads",
                                            "Facebook", "LinkedIn", "JustDial", "Print", "Other"])
        status = c2.selectbox("Status", ["Planning", "Active", "Paused", "Completed"])
        budget = c2.number_input("Budget (₹)", min_value=0.0, step=500.0)
        spent = c3.number_input("Spent (₹)", min_value=0.0, step=500.0)
        leads = c3.number_input("Leads", min_value=0, step=1)
        convs = c3.number_input("Conversions", min_value=0, step=1)
        start = c1.date_input("Start Date")
        end = c2.date_input("End Date")
        if st.button("💾 Save Campaign", type="primary"):
            new_camp = pd.DataFrame([{
                "Campaign": camp_name, "Channel": channel, "Status": status,
                "Budget": budget, "Spent": spent, "Leads": leads, "Conversions": convs,
                "Start": str(start), "End": str(end)
            }])
            st.session_state.campaigns = pd.concat(
                [st.session_state.campaigns, new_camp], ignore_index=True)
            st.success("✅ Campaign saved!")
            st.rerun()

# ── TAB 3: CONTENT CALENDAR ────────────────────────────────────
with tabs[2]:
    st.subheader("📅 Content Calendar")
    cc_df = st.session_state.content_calendar.copy()

    status_color = {"Scheduled": "🟢", "Draft": "🟡", "Posted": "✅", "Cancelled": "🔴"}
    cc_df["Status"] = cc_df["Status"].map(lambda s: f"{status_color.get(s, '')} {s}")
    st.dataframe(cc_df, use_container_width=True, hide_index=True)

    SEASONAL = [
        ("May", "Eid al-Adha", "Export textiles, gifting, apparels"),
        ("Jun", "End of Q1", "B2B bulk deals, clearance offers"),
        ("Aug", "Independence Day", "Tricolour campaigns, patriotic discounts"),
        ("Aug", "Raksha Bandhan", "Gifts, fashion, sweets"),
        ("Oct", "Navratri / Dussehra", "Fashion, electronics, home goods"),
        ("Nov", "Diwali", "Biggest sale season — all categories"),
        ("Dec", "Year End Sale", "Clearance, gifting, corporate orders"),
    ]
    st.subheader("🎆 Upcoming Seasonal Opportunities")
    for month, event, opp in SEASONAL:
        cols = st.columns([1, 2, 3])
        cols[0].markdown(f"**{month}**")
        cols[1].markdown(event)
        cols[2].caption(opp)

    with st.expander("➕ Add Content Piece"):
        ct1, ct2 = st.columns(2)
        ct_date = ct1.date_input("Date", value=date.today() + timedelta(days=3))
        ct_platform = ct1.selectbox("Platform", ["Instagram", "WhatsApp", "LinkedIn",
                                                   "Facebook", "YouTube", "Twitter/X"])
        ct_type = ct2.selectbox("Content Type", ["Product Post", "Promo Broadcast",
                                                   "Industry Article", "Customer Story",
                                                   "Festival Post", "Export Showcase"])
        ct_caption = ct2.text_area("Caption / Brief", height=80)
        ct_status = ct1.selectbox("Status", ["Draft", "Scheduled", "Posted"])
        if st.button("➕ Add to Calendar", type="primary"):
            new_ct = pd.DataFrame([{"Date": str(ct_date), "Platform": ct_platform,
                                     "Type": ct_type, "Caption": ct_caption, "Status": ct_status}])
            st.session_state.content_calendar = pd.concat(
                [st.session_state.content_calendar, new_ct], ignore_index=True)
            st.success("✅ Added!")
            st.rerun()

# ── TAB 4: MESSAGE TEMPLATES ───────────────────────────────────
with tabs[3]:
    st.subheader("📧 Ready-to-Use Message Templates")
    template_type = st.selectbox("Template Type", [
        "WhatsApp – New Product Launch",
        "WhatsApp – Festival Offer",
        "WhatsApp – Payment Reminder",
        "WhatsApp – Export Inquiry Response",
        "Email – Follow-up After Meeting",
        "Email – Cold Outreach to Buyer",
        "LinkedIn – Export Connection Request",
        "SMS – Order Confirmation",
    ])
    biz = "Your Business"

    TEMPLATES = {
        "WhatsApp – New Product Launch": f"""🎉 *New Launch — {biz}*

We're excited to introduce: *[PRODUCT NAME]*

✅ [Key Feature 1]
✅ [Key Feature 2]
✅ [Key Feature 3]

💰 Introductory Price: ₹[PRICE]
📦 Min Order: [MOQ]

Reply *YES* to receive catalogue 📋

📞 {biz} | [Phone]""",

        "WhatsApp – Festival Offer": f"""🪔 *Festival Special — {biz}* 🎁

This [FESTIVAL], get *[X]% OFF* on all orders!

🛍️ Valid till: [DATE]
💳 Min order: ₹[AMOUNT]
🚚 Free delivery above ₹[THRESHOLD]

Place your order now → Reply or Call
📞 [Phone]""",

        "WhatsApp – Payment Reminder": """Dear [Customer Name] 🙏

Friendly reminder: Payment of *₹[AMOUNT]* for Invoice *#[INV]* was due on *[DATE]*.

Please arrange at your earliest convenience:
• UPI: [UPI_ID]
• Bank: [ACCOUNT]

Thank you!""",

        "WhatsApp – Export Inquiry Response": """Dear [Buyer Name],

Thank you for your inquiry about [Product].

We can supply:
✅ Qty: As per your requirement
✅ Quality: [Grade/Standard]
✅ Lead Time: [X] days
✅ Payment: LC / TT / PayPal
✅ Certification: [ISO/BIS/etc]

Can we schedule a call this week?

[Your Name] | [Company] | [Country]""",

        "Email – Cold Outreach to Buyer": """Subject: [Product] Supply Offer from India | [Your Company]

Dear [Buyer Name],

I'm reaching out from [Company], a leading exporter of [Product] based in India.

We supply to [Country 1], [Country 2], and are looking to expand to [Target Country].

Why us:
• [Price advantage]
• [Quality certification]
• [Delivery track record]

Could we send you a product sample and pricing sheet?

Warm regards,
[Name] | [Company] | [Email] | [Phone]""",
    }

    template = TEMPLATES.get(template_type,
                              "Select a template type from the dropdown above.")
    st.text_area("📋 Template (click to copy & edit)", template, height=300)
    st.download_button("⬇️ Download Template", template,
                       file_name=f"template_{template_type[:20].replace(' ','_')}.txt")

# ── TAB 5: CUSTOMER SEGMENTS ───────────────────────────────────
with tabs[4]:
    st.subheader("🏆 Customer Segmentation")
    st.caption("Segment your customers for targeted marketing")

    segments = pd.DataFrame([
        {"Segment": "🥇 Champions", "Criteria": "Bought recently, high frequency, high value",
         "Action": "Reward & ask for referrals", "Count": 8},
        {"Segment": "💎 Loyal", "Criteria": "Buy regularly, good value",
         "Action": "Upsell premium products", "Count": 14},
        {"Segment": "🌱 Potential", "Criteria": "Recent buyers, not yet frequent",
         "Action": "Nurture with offers + content", "Count": 22},
        {"Segment": "😴 At Risk", "Criteria": "Used to buy, gone quiet > 60 days",
         "Action": "Win-back WhatsApp campaign", "Count": 11},
        {"Segment": "💤 Lost", "Criteria": "No purchase in 6+ months",
         "Action": "Big discount re-engagement", "Count": 7},
        {"Segment": "🆕 New", "Criteria": "First purchase in last 30 days",
         "Action": "Onboarding sequence + thank you", "Count": 9},
    ])
    st.dataframe(segments, use_container_width=True, hide_index=True)

    fig_seg = px.pie(segments, values="Count", names="Segment",
                     title="Customer Base Distribution",
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_seg, use_container_width=True)

    st.subheader("🎯 Segment-Specific Campaign Ideas")
    seg_sel = st.selectbox("Pick Segment", segments["Segment"].tolist())
    ideas = {
        "🥇 Champions": "Send personalised thank-you gift. Ask for Google review. Offer referral bonus of ₹500 for each new customer they bring.",
        "💎 Loyal": "Early access to new products. Loyalty discount card. Bundle deal: buy 5 get 1 free.",
        "🌱 Potential": "Educational WhatsApp series about your products. Free sample offer. Invite to factory visit.",
        "😴 At Risk": "We miss you message + 15% comeback discount. Survey: what would bring them back?",
        "💤 Lost": "30% clearance offer. New product announcement. Personal call from owner.",
        "🆕 New": "Welcome message + product catalogue. Tips for using the product. Follow-up at 7, 14, 30 days.",
    }
    st.info(ideas.get(seg_sel, ""))
