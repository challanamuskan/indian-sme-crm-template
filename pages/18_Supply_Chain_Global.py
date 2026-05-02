import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json

st.set_page_config(page_title="🌐 Global Supply Chain", layout="wide")

# ─── Auth Guard ───────────────────────────────────────────────
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login first")
    st.stop()

# ─── Industry → Trade Connections Map ─────────────────────────
INDUSTRY_TRADE_MAP = {
    "Textile & Garments": {
        "export_markets": ["USA", "EU", "UAE", "UK", "Japan", "Australia", "Canada"],
        "import_sources": ["China", "Bangladesh", "Vietnam", "Turkey", "Indonesia"],
        "key_products": ["cotton yarn", "fabric bolts", "readymade garments", "denim", "silk"],
        "global_buyers": ["H&M Sourcing", "Walmart Global", "Marks & Spencer", "Zara Inditex", "Target Corp"],
        "global_suppliers": ["Alibaba.com suppliers", "Global Sources", "Made-in-China.com", "TradeIndia"],
        "trade_portals": ["https://www.fibre2fashion.com", "https://www.textilescommittee.gov.in"],
        "export_incentives": ["RoSCTL", "TUFS", "PLI Scheme for Textiles", "ATUFS"],
    },
    "Textile Machinery Parts": {
        "export_markets": ["Bangladesh", "Pakistan", "Sri Lanka", "Vietnam", "Ethiopia", "Egypt"],
        "import_sources": ["Germany", "Japan", "Switzerland", "Italy", "China"],
        "key_products": ["loom parts", "spindle assemblies", "gear sets", "bearings", "shuttles"],
        "global_buyers": ["Groz-Beckert", "Picanol", "Toyota Industries", "Vandewiele", "Dornier GmbH"],
        "global_suppliers": ["SKF India", "Bosch Rexroth", "INA Bearings", "NSK Ltd"],
        "trade_portals": ["https://www.indiamart.com", "https://www.tradeindia.com"],
        "export_incentives": ["MEIS", "RoDTEP", "Advance Authorization Scheme"],
    },
    "Pharmaceuticals": {
        "export_markets": ["USA", "UK", "South Africa", "Russia", "Brazil", "Nigeria", "Kenya"],
        "import_sources": ["China", "USA", "Germany", "Italy", "Japan"],
        "key_products": ["generics", "APIs", "formulations", "OTC drugs", "nutraceuticals"],
        "global_buyers": ["WHO", "USAID", "Medicines Sans Frontiers", "McKesson", "AmerisourceBergen"],
        "global_suppliers": ["Divi's Laboratories", "Dr. Reddy's API Division", "Cipla API"],
        "trade_portals": ["https://www.pharmexcil.org", "https://www.plexconcil.org"],
        "export_incentives": ["PLI Pharma", "MEIS", "Pharma clusters scheme"],
    },
    "Engineering & Auto Parts": {
        "export_markets": ["USA", "Germany", "UK", "South Korea", "Japan", "Brazil", "Mexico"],
        "import_sources": ["China", "Japan", "Germany", "South Korea", "Taiwan"],
        "key_products": ["castings", "forgings", "auto components", "precision parts", "hydraulic parts"],
        "global_buyers": ["Bosch", "Delphi Technologies", "Continental AG", "Magna International", "ZF Group"],
        "global_suppliers": ["Tata AutoComp", "Bharat Forge", "Mahle", "Valeo"],
        "trade_portals": ["https://www.acma.in", "https://www.eepcIndia.org"],
        "export_incentives": ["RoDTEP", "PLI Auto", "FAME II"],
    },
    "Agri & Food Processing": {
        "export_markets": ["USA", "UAE", "UK", "Netherlands", "Saudi Arabia", "Bangladesh", "Malaysia"],
        "import_sources": ["Brazil", "Argentina", "Australia", "Ukraine", "USA"],
        "key_products": ["basmati rice", "spices", "processed pulses", "mango pulp", "sugar"],
        "global_buyers": ["Olam International", "LDC", "Cargill", "ITC Agri", "SAFAL"],
        "global_suppliers": ["ITC Agri", "Adani Wilmar", "Ruchi Soya", "Godrej Agrovet"],
        "trade_portals": ["https://www.apeda.gov.in", "https://www.nafed-india.com"],
        "export_incentives": ["APEDA subsidies", "Market Access Initiative", "Transport subsidy"],
    },
    "IT & Software Services": {
        "export_markets": ["USA", "UK", "EU", "Australia", "Canada", "Singapore", "UAE"],
        "import_sources": ["USA (cloud)", "Germany (SAP)", "Oracle", "Microsoft", "AWS"],
        "key_products": ["custom software", "AI/ML services", "BPO", "SaaS products", "app dev"],
        "global_buyers": ["TCS", "Infosys", "Wipro", "NASSCOM members", "Fortune 500 IT budgets"],
        "global_suppliers": ["AWS", "Azure", "Google Cloud", "Salesforce", "SAP"],
        "trade_portals": ["https://www.nasscom.in", "https://www.esoftexport.com"],
        "export_incentives": ["STPI scheme", "SEZ tax benefits", "SEIS for service exports"],
    },
    "Chemicals & Dyes": {
        "export_markets": ["USA", "Brazil", "EU", "Turkey", "South Korea", "Mexico"],
        "import_sources": ["China", "Germany", "USA", "Netherlands", "Japan"],
        "key_products": ["reactive dyes", "disperse dyes", "specialty chemicals", "pigments"],
        "global_buyers": ["Archroma", "Huntsman Corp", "DyStar", "Bezema", "Clariant"],
        "global_suppliers": ["Huntsman India", "Atul Ltd", "Gujarat Fluorochemicals", "Aarti Industries"],
        "trade_portals": ["https://www.chemexcil.gov.in", "https://www.plexconcil.org"],
        "export_incentives": ["RoDTEP", "MEIS", "Chemical PLI"],
    },
    "Handicrafts & Gems": {
        "export_markets": ["USA", "UAE", "EU", "UK", "Japan", "Hong Kong", "Singapore"],
        "import_sources": ["Africa (raw gems)", "Belgium", "Israel", "Thailand", "China"],
        "key_products": ["cut diamonds", "gemstone jewellery", "silver jewellery", "handicrafts"],
        "global_buyers": ["Swarovski", "Tiffany & Co", "Pandora", "LVMH", "Signet Jewelers"],
        "global_suppliers": ["Gitanjali Gems", "Malabar Gold", "TBZ", "Shrenuj & Co"],
        "trade_portals": ["https://www.gjepc.org", "https://www.epch.in"],
        "export_incentives": ["DEPB", "ATA Carnet", "Gem & Jewellery export incentives"],
    },
}

# ─── Inventory DB (session state) ─────────────────────────────
def init_inventory():
    if "raw_inventory" not in st.session_state:
        st.session_state.raw_inventory = pd.DataFrame([
            {"Item": "Cotton Yarn 30s", "Category": "Raw Material", "Stock_Qty": 500, "Unit": "kg",
             "Min_Level": 100, "Max_Level": 1000, "Cost_Price": 85.0, "Supplier": "Vardhman Mills",
             "Last_Updated": "2026-04-01", "Location": "Warehouse A"},
            {"Item": "Loom Shuttle Set", "Category": "Machinery Part", "Stock_Qty": 45, "Unit": "pcs",
             "Min_Level": 20, "Max_Level": 200, "Cost_Price": 320.0, "Supplier": "Picanol BE",
             "Last_Updated": "2026-03-28", "Location": "Store Room"},
        ])
    if "finished_inventory" not in st.session_state:
        st.session_state.finished_inventory = pd.DataFrame([
            {"Item": "Grey Fabric 60\"", "Category": "Finished Good", "Stock_Qty": 2000, "Unit": "meters",
             "Min_Level": 500, "Max_Level": 10000, "Sale_Price": 45.0, "Target_Market": "UAE",
             "Last_Updated": "2026-04-02", "Location": "Finished Goods Store"},
            {"Item": "Processed Denim", "Category": "Finished Good", "Stock_Qty": 800, "Unit": "meters",
             "Min_Level": 200, "Max_Level": 5000, "Sale_Price": 125.0, "Target_Market": "USA",
             "Last_Updated": "2026-04-01", "Location": "Finished Goods Store"},
        ])
    if "trade_connections" not in st.session_state:
        st.session_state.trade_connections = []

init_inventory()

# ─── UI ───────────────────────────────────────────────────────
st.title("🌐 Global Supply Chain & Trade Hub")
st.caption("Find global buyers & suppliers • Manage dual-level inventory • Market yourself globally")

tabs = st.tabs([
    "🔍 Find Global Connections",
    "📦 Raw Material Inventory",
    "✅ Finished Goods Inventory",
    "📣 Self-Marketing & Outreach",
    "📊 Supply Chain Dashboard"
])

# ══════════════════════════════════════════════════════════════
# TAB 1: FIND GLOBAL CONNECTIONS
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("🔍 Find Global Exporters & Importers")

    col1, col2 = st.columns([1, 2])
    with col1:
        industry = st.selectbox("Your Industry", list(INDUSTRY_TRADE_MAP.keys()))
        mode = st.radio("Looking to:", ["Export (find buyers)", "Import (find suppliers)", "Both"])
        search_btn = st.button("🔍 Find Connections", type="primary", use_container_width=True)

    if search_btn:
        data = INDUSTRY_TRADE_MAP[industry]

        with col2:
            if mode in ["Export (find buyers)", "Both"]:
                st.markdown("### 🟢 Export Markets (Where You Can Sell)")
                mkt_df = pd.DataFrame({
                    "Country": data["export_markets"],
                    "Potential": ["High" if i < 3 else "Medium" if i < 5 else "Growing"
                                  for i in range(len(data["export_markets"]))]
                })
                st.dataframe(mkt_df, use_container_width=True, hide_index=True)

                st.markdown("#### 🏢 Known Global Buyers")
                for buyer in data["global_buyers"]:
                    st.markdown(f"- `{buyer}`")

            if mode in ["Import (find suppliers)", "Both"]:
                st.markdown("### 🔵 Import Sources (Where You Can Buy)")
                src_df = pd.DataFrame({
                    "Country": data["import_sources"],
                    "Type": ["Primary" if i < 2 else "Secondary" for i in range(len(data["import_sources"]))]
                })
                st.dataframe(src_df, use_container_width=True, hide_index=True)

                st.markdown("#### 🏭 Key Global Suppliers")
                for sup in data["global_suppliers"]:
                    st.markdown(f"- `{sup}`")

        st.divider()
        col3, col4 = st.columns(2)
        with col3:
            st.markdown("### 📋 Key Products")
            for p in data["key_products"]:
                st.markdown(f"• {p}")
        with col4:
            st.markdown("### 🔗 Trade Portals")
            for portal in data["trade_portals"]:
                st.markdown(f"[{portal}]({portal})")
            st.markdown("### 💰 Export Incentives (India)")
            for inc in data["export_incentives"]:
                st.markdown(f"• {inc}")

        # Map visualization
        if mode in ["Export (find buyers)", "Both"]:
            st.markdown("### 🗺️ Export Market Map")
            country_coords = {
                "USA": (37.09, -95.71), "UK": (55.37, -3.43), "EU": (50.85, 4.35),
                "Germany": (51.16, 10.45), "UAE": (23.42, 53.84), "Japan": (36.20, 138.25),
                "Bangladesh": (23.68, 90.35), "China": (35.86, 104.19), "Vietnam": (14.05, 108.27),
                "Australia": (-25.27, 133.77), "Canada": (56.13, -106.34), "Brazil": (-14.23, -51.92),
                "South Africa": (-30.55, 22.93), "Singapore": (1.35, 103.82), "Pakistan": (30.37, 69.34),
                "Sri Lanka": (7.87, 80.77), "Ethiopia": (9.14, 40.48), "Egypt": (26.82, 30.80),
                "Turkey": (38.96, 35.24), "Netherlands": (52.13, 5.29), "Saudi Arabia": (23.88, 45.07),
                "Malaysia": (4.21, 101.97), "South Korea": (35.90, 127.76), "Mexico": (23.63, -102.55),
                "Nigeria": (9.08, 8.67), "Kenya": (-0.02, 37.90), "Russia": (61.52, 105.31),
                "Belgium": (50.50, 4.46), "Israel": (31.04, 34.85), "Thailand": (15.87, 100.99),
                "Hong Kong": (22.39, 114.10), "Italy": (41.87, 12.56), "Indonesia": (-0.78, 113.92),
                "Argentina": (-38.41, -63.61), "Ukraine": (48.37, 31.16), "Taiwan": (23.69, 120.96),
            }
            coords = [(country_coords[c][0], country_coords[c][1], c)
                      for c in data["export_markets"] if c in country_coords]
            if coords:
                map_df = pd.DataFrame(coords, columns=["lat", "lon", "Country"])
                fig = px.scatter_geo(map_df, lat="lat", lon="lon", text="Country",
                                     title=f"Export Markets for {industry}",
                                     projection="natural earth")
                fig.update_traces(textposition="top center", marker=dict(size=10, color="#FF6B35"))
                fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig, use_container_width=True)

    # ── Add Connection ──
    st.divider()
    st.subheader("➕ Log a Trade Connection")
    with st.expander("Add New Global Contact"):
        c1, c2, c3 = st.columns(3)
        with c1:
            conn_name = st.text_input("Company / Contact Name")
            conn_country = st.text_input("Country")
        with c2:
            conn_type = st.selectbox("Type", ["Buyer", "Supplier", "Distributor", "Agent", "Partner"])
            conn_industry = st.selectbox("Industry", list(INDUSTRY_TRADE_MAP.keys()))
        with c3:
            conn_email = st.text_input("Email")
            conn_status = st.selectbox("Status", ["Prospect", "Contacted", "Negotiating", "Active", "On Hold"])
        conn_notes = st.text_area("Notes", height=60)
        if st.button("💾 Save Connection", type="primary"):
            st.session_state.trade_connections.append({
                "Company": conn_name, "Country": conn_country, "Type": conn_type,
                "Industry": conn_industry, "Email": conn_email, "Status": conn_status,
                "Notes": conn_notes, "Added": str(date.today())
            })
            st.success(f"✅ {conn_name} saved!")

    if st.session_state.trade_connections:
        st.subheader("📋 Your Trade Connections")
        conn_df = pd.DataFrame(st.session_state.trade_connections)
        st.dataframe(conn_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════
# TAB 2: RAW MATERIAL INVENTORY
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("📦 Raw Material Inventory")

    col_a, col_b, col_c = st.columns(3)
    raw_df = st.session_state.raw_inventory
    low_stock = raw_df[raw_df["Stock_Qty"] <= raw_df["Min_Level"]]
    col_a.metric("Total Items", len(raw_df))
    col_b.metric("Low Stock Alerts", len(low_stock), delta=f"-{len(low_stock)} items" if len(low_stock) else None,
                 delta_color="inverse")
    col_c.metric("Total Value (₹)", f"₹{(raw_df['Stock_Qty'] * raw_df['Cost_Price']).sum():,.0f}")

    if len(low_stock):
        st.warning(f"⚠️ {len(low_stock)} item(s) below minimum level!")
        st.dataframe(low_stock[["Item", "Stock_Qty", "Min_Level", "Supplier"]], use_container_width=True, hide_index=True)

    st.dataframe(
        raw_df.style.apply(
            lambda r: ["background-color: #fff3cd" if r["Stock_Qty"] <= r["Min_Level"] else "" for _ in r],
            axis=1
        ),
        use_container_width=True, hide_index=True
    )

    st.subheader("➕ Add / Update Raw Material")
    with st.expander("Stock Entry Form"):
        r1, r2, r3 = st.columns(3)
        with r1:
            item_name = st.text_input("Item Name", key="raw_item")
            category = st.selectbox("Category", ["Raw Material", "Packing Material", "Machinery Part", "Chemical", "Other"])
            qty = st.number_input("Quantity", min_value=0.0, step=1.0)
        with r2:
            unit = st.selectbox("Unit", ["kg", "pcs", "liters", "meters", "tons", "boxes"])
            min_lvl = st.number_input("Min Level", min_value=0.0, step=1.0)
            max_lvl = st.number_input("Max Level", min_value=0.0, step=1.0)
        with r3:
            cost = st.number_input("Cost Price (₹)", min_value=0.0, step=0.5)
            supplier = st.text_input("Supplier Name")
            location = st.text_input("Storage Location")
        if st.button("💾 Save Raw Material Entry", type="primary"):
            new_row = pd.DataFrame([{
                "Item": item_name, "Category": category, "Stock_Qty": qty,
                "Unit": unit, "Min_Level": min_lvl, "Max_Level": max_lvl,
                "Cost_Price": cost, "Supplier": supplier,
                "Last_Updated": str(date.today()), "Location": location
            }])
            st.session_state.raw_inventory = pd.concat(
                [st.session_state.raw_inventory, new_row], ignore_index=True)
            st.success("✅ Entry saved!")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 3: FINISHED GOODS INVENTORY
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.subheader("✅ Finished Goods Inventory")

    fin_df = st.session_state.finished_inventory
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total SKUs", len(fin_df))
    col_b.metric("Total Value (₹)", f"₹{(fin_df['Stock_Qty'] * fin_df['Sale_Price']).sum():,.0f}")
    low_fin = fin_df[fin_df["Stock_Qty"] <= fin_df["Min_Level"]]
    col_c.metric("Low Stock Alerts", len(low_fin))

    st.dataframe(fin_df, use_container_width=True, hide_index=True)

    # Stock flow chart
    fig_bar = px.bar(fin_df, x="Item", y="Stock_Qty",
                     color="Target_Market", title="Finished Goods by Target Export Market",
                     color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.subheader("➕ Add Finished Good")
    with st.expander("Finished Goods Entry"):
        f1, f2, f3 = st.columns(3)
        with f1:
            fg_item = st.text_input("Product Name", key="fg_item")
            fg_cat = st.selectbox("Category", ["Finished Good", "Semi-Finished", "By-Product", "Export Grade"])
            fg_qty = st.number_input("Quantity", min_value=0.0, step=1.0, key="fg_qty")
        with f2:
            fg_unit = st.selectbox("Unit", ["meters", "kg", "pcs", "boxes", "tons"], key="fg_unit")
            fg_min = st.number_input("Min Level", min_value=0.0, key="fg_min")
            fg_max = st.number_input("Max Level", min_value=0.0, key="fg_max")
        with f3:
            fg_price = st.number_input("Sale Price (₹)", min_value=0.0, step=0.5, key="fg_price")
            fg_market = st.selectbox("Target Market", ["India", "UAE", "USA", "EU", "UK", "Bangladesh",
                                                       "Africa", "Southeast Asia", "Australia", "Canada"])
            fg_location = st.text_input("Location", key="fg_loc")
        if st.button("💾 Save Finished Good", type="primary"):
            new_fg = pd.DataFrame([{
                "Item": fg_item, "Category": fg_cat, "Stock_Qty": fg_qty, "Unit": fg_unit,
                "Min_Level": fg_min, "Max_Level": fg_max, "Sale_Price": fg_price,
                "Target_Market": fg_market, "Last_Updated": str(date.today()), "Location": fg_location
            }])
            st.session_state.finished_inventory = pd.concat(
                [st.session_state.finished_inventory, new_fg], ignore_index=True)
            st.success("✅ Finished good saved!")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 4: SELF-MARKETING & OUTREACH
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("📣 Market Yourself Globally")
    st.info("📋 Generate professional trade inquiry responses, export pitch emails, and listing descriptions")

    industry_sel = st.selectbox("Your Industry", list(INDUSTRY_TRADE_MAP.keys()), key="mkt_industry")
    pitch_type = st.selectbox("Generate:", [
        "Export Pitch Email (to foreign buyer)",
        "Import Inquiry (to foreign supplier)",
        "Trade Portal Listing Description",
        "B2B WhatsApp Intro Message",
        "LinkedIn Outreach for Export Lead",
    ])

    c1, c2 = st.columns(2)
    with c1:
        biz_name = st.text_input("Your Business Name", value="Sharma Traders")
        biz_city = st.text_input("City", value="Jaipur, Rajasthan, India")
    with c2:
        target_country = st.text_input("Target Country / Buyer", value="UAE")
        product = st.text_input("Your Main Product", value=INDUSTRY_TRADE_MAP[industry_sel]["key_products"][0])

    if st.button("✍️ Generate Pitch", type="primary"):
        data_m = INDUSTRY_TRADE_MAP[industry_sel]
        if pitch_type == "Export Pitch Email (to foreign buyer)":
            pitch = f"""Subject: Export Inquiry – {product} from India | {biz_name}

Dear Sir/Madam,

I am reaching out from **{biz_name}**, a leading manufacturer/trader of {product} based in {biz_city}, India.

We are currently seeking to establish long-term export partnerships in **{target_country}** and believe there is strong alignment with your import requirements.

**Our Offering:**
• Product: {product}
• Key export markets we serve: {', '.join(data_m['export_markets'][:3])}
• Competitive pricing with GST-compliant invoicing
• MSME registered | DPIIT recognised | Export-ready

We would love to share our product catalog, pricing sheet, and compliance documents.

Could we schedule a 15-minute call this week?

Warm regards,
[Your Name] | {biz_name}
{biz_city} | [Phone] | [Email]
"""
        elif pitch_type == "Trade Portal Listing Description":
            pitch = f"""**{biz_name}** – {industry_sel} Manufacturer & Exporter, {biz_city}

Established Indian exporter of high-quality {product}. Supplying to {', '.join(data_m['export_markets'][:4])}.

✓ MSME Registered | ✓ GST Compliant | ✓ Export-ready
✓ Min. Order: [MOQ] | ✓ Lead Time: [X days] | ✓ Payment: LC / TT / PayPal

**Products:** {', '.join(data_m['key_products'][:3])}
**Certifications:** [ISO / BIS / APEDA / etc.]

Contact: [email] | [phone] | [website]
"""
        else:
            pitch = f"""Hi,

I'm from {biz_name}, {biz_city} — we manufacture/supply {product} for {industry_sel} companies.

Looking to connect with buyers/importers in {target_country}.

Can we discuss how we can work together?

Thanks,
{biz_name}"""

        st.text_area("📧 Generated Pitch", pitch, height=300)
        st.download_button("⬇️ Download Pitch", pitch, file_name="trade_pitch.txt")

    st.divider()
    st.subheader("🌐 Key Trade Portals to List Your Business")
    portals = [
        ("IndiaMART", "https://seller.indiamart.com", "Largest Indian B2B marketplace"),
        ("TradeIndia", "https://www.tradeindia.com", "SME-focused global trade directory"),
        ("Alibaba", "https://supplier.alibaba.com", "World's largest B2B platform"),
        ("Global Sources", "https://www.globalsources.com", "Hong Kong-based verified supplier platform"),
        ("EC21", "https://www.ec21.com", "Korean global trade platform"),
        ("ExportHub", "https://www.exporthub.com", "Verified exporter directory"),
        ("Kompass", "https://in.kompass.com", "European B2B directory"),
        ("FIEO", "https://www.fieo.org", "Federation of Indian Export Organisations"),
    ]
    for name, url, desc in portals:
        col_l, col_r = st.columns([1, 3])
        col_l.markdown(f"**[{name}]({url})**")
        col_r.caption(desc)

# ══════════════════════════════════════════════════════════════
# TAB 5: SUPPLY CHAIN DASHBOARD
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("📊 Supply Chain Overview")

    raw_df = st.session_state.raw_inventory
    fin_df = st.session_state.finished_inventory

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Raw Materials (SKUs)", len(raw_df))
    col2.metric("Finished Goods (SKUs)", len(fin_df))
    raw_val = (raw_df["Stock_Qty"] * raw_df["Cost_Price"]).sum()
    fin_val = (fin_df["Stock_Qty"] * fin_df["Sale_Price"]).sum()
    col3.metric("Raw Inventory Value", f"₹{raw_val:,.0f}")
    col4.metric("Finished Goods Value", f"₹{fin_val:,.0f}")

    col_l, col_r = st.columns(2)
    with col_l:
        fig_raw = px.pie(raw_df, values="Stock_Qty", names="Category",
                         title="Raw Material by Category")
        st.plotly_chart(fig_raw, use_container_width=True)
    with col_r:
        fig_fin = px.bar(fin_df, x="Item", y=fin_df["Stock_Qty"] * fin_df["Sale_Price"],
                         title="Finished Goods Value by SKU",
                         labels={"y": "Value (₹)"})
        st.plotly_chart(fig_fin, use_container_width=True)

    # Combined inventory table
    st.subheader("🔄 Combined Inventory Health")
    combined = []
    for _, r in raw_df.iterrows():
        pct = (r["Stock_Qty"] / r["Max_Level"] * 100) if r["Max_Level"] > 0 else 0
        status = "🔴 Low" if r["Stock_Qty"] <= r["Min_Level"] else "🟡 Mid" if pct < 60 else "🟢 Good"
        combined.append({"Type": "Raw", "Item": r["Item"], "Qty": r["Stock_Qty"],
                          "Unit": r["Unit"], "Fill %": f"{pct:.0f}%", "Status": status})
    for _, r in fin_df.iterrows():
        pct = (r["Stock_Qty"] / r["Max_Level"] * 100) if r["Max_Level"] > 0 else 0
        status = "🔴 Low" if r["Stock_Qty"] <= r["Min_Level"] else "🟡 Mid" if pct < 60 else "🟢 Good"
        combined.append({"Type": "Finished", "Item": r["Item"], "Qty": r["Stock_Qty"],
                          "Unit": r["Unit"], "Fill %": f"{pct:.0f}%", "Status": status})
    st.dataframe(pd.DataFrame(combined), use_container_width=True, hide_index=True)

    if st.session_state.trade_connections:
        st.subheader("🤝 Trade Connections Summary")
        conn_df = pd.DataFrame(st.session_state.trade_connections)
        fig_conn = px.bar(conn_df.groupby(["Type", "Status"]).size().reset_index(name="Count"),
                          x="Type", y="Count", color="Status",
                          title="Trade Connections by Type & Status")
        st.plotly_chart(fig_conn, use_container_width=True)
