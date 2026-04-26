"""pages/17_Promotions.py — WhatsApp bulk broadcast, offer builder, seasonal campaigns."""

import streamlit as st
import urllib.parse
import pandas as pd
from utils.config_loader import load_config
from utils.db import get_all_records

cfg = load_config()
biz = cfg["business"]
st.title("🎯 Promotions & Broadcast")
st.caption("Create offers, generate WhatsApp broadcast links, track campaign results.")

tab1, tab2, tab3 = st.tabs(["📱 WhatsApp Broadcast", "🎁 Offer Builder", "📅 Seasonal Calendar"])

# ── Tab 1: WhatsApp Broadcast ─────────────────────────────────────────────────
with tab1:
    st.subheader("📱 WhatsApp Broadcast Generator")
    st.info("Generates a personalised wa.me link per customer. Click each to open WhatsApp and send.")

    message_template = st.text_area("Message Template", height=120,
        value=f"Namaste {{name}}! 🙏\n\nSpecial offer from {biz['name']}:\n👉 [YOUR OFFER HERE]\n\nValid till [DATE]. Reply to order!\n\n— {biz['name']}\n📞 {biz['phone']}")

    try:
        customers = get_all_records("customers")
        if customers:
            df_c = pd.DataFrame(customers)
            selected = st.multiselect("Select customers", df_c["name"].tolist(),
                                       default=df_c["name"].tolist()[:5])
            if selected and st.button("🔗 Generate Broadcast Links"):
                selected_customers = df_c[df_c["name"].isin(selected)]
                st.subheader("Broadcast Links")
                for _, row in selected_customers.iterrows():
                    phone = str(row.get("phone","")).replace("+","").replace(" ","").replace("-","")
                    msg   = message_template.replace("{name}", row["name"])
                    url   = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                    st.markdown(f"**{row['name']}** ({row.get('phone','no phone')}) — [📲 Send WhatsApp]({url})")
        else:
            st.info("No customers yet. Add customers first.")
    except Exception as e:
        st.error(f"Error loading customers: {e}")

# ── Tab 2: Offer Builder ──────────────────────────────────────────────────────
with tab2:
    st.subheader("🎁 Offer Builder")
    col1, col2 = st.columns(2)
    offer_type = col1.selectbox("Offer Type", ["Flat Discount", "% Discount", "Buy X Get Y", "Bundle Deal", "Clearance Sale", "Festival Special"])
    product    = col1.text_input("Product / Category")
    discount   = col2.number_input("Discount Value", min_value=0.0)
    disc_type  = col2.radio("Type", ["₹ Flat", "% Off"], horizontal=True)
    valid_till = col2.date_input("Valid Till")
    extra_note = st.text_input("Additional note (e.g. 'Min order ₹500')")

    if st.button("Generate Offer Message"):
        disc_str = f"₹{discount:.0f} off" if disc_type == "₹ Flat" else f"{discount:.0f}% off"
        msg = f"""🎉 *Special Offer — {biz['name']}* 🎉

{offer_type}: *{disc_str}* on {product}
📅 Valid till: {valid_till.strftime('%d %b %Y')}
{f'📌 {extra_note}' if extra_note else ''}

📞 Call/WhatsApp: {biz['phone']}
To order, just reply with your requirement!"""
        st.text_area("Your Offer Message (copy & send)", msg, height=180)

# ── Tab 3: Seasonal Calendar ──────────────────────────────────────────────────
with tab3:
    st.subheader("📅 Indian Business Events & Seasonal Opportunities")
    events = [
        {"Month":"Jan","Event":"Makar Sankranti / Lohri","Opportunity":"Sweets, textiles, gifts"},
        {"Month":"Feb","Event":"Valentine's Day","Opportunity":"Gifts, flowers, F&B"},
        {"Month":"Mar","Event":"Holi","Opportunity":"Colours, FMCG, fashion"},
        {"Month":"Apr","Event":"New Financial Year","Opportunity":"B2B deals, bulk orders"},
        {"Month":"Apr","Event":"Gudi Padwa / Ugadi","Opportunity":"New purchases, home goods"},
        {"Month":"Aug","Event":"Independence Day","Opportunity":"Tricolour campaigns, discounts"},
        {"Month":"Aug","Event":"Raksha Bandhan","Opportunity":"Gifts, sweets, fashion"},
        {"Month":"Sep","Event":"Ganesh Chaturthi","Opportunity":"Pooja items, food, decoration"},
        {"Month":"Oct","Event":"Navratri / Dussehra","Opportunity":"Fashion, electronics, home"},
        {"Month":"Nov","Event":"Diwali","Opportunity":"Biggest sale season — all categories"},
        {"Month":"Nov","Event":"Bhai Dooj","Opportunity":"Gifts, sweets"},
        {"Month":"Dec","Event":"Christmas / Year End","Opportunity":"Offers, clearance, gifting"},
    ]
    st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)
    st.caption("Plan your WhatsApp broadcasts and ad campaigns 2 weeks before each event.")
