# 🏪 Indian SME & HNI Growth Platform

> From CRM to full business OS — built for Indian small businesses, growing enterprises, and high-net-worth clients who want AI-powered growth tools without enterprise pricing.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-crm--template.streamlit.app-FF4B4B?style=flat-square&logo=streamlit)](https://crm-template.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat-square&logo=supabase)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Built for India](https://img.shields.io/badge/Built%20for-Indian%20SMEs%20🇮🇳-orange?style=flat-square)](https://challanamuskan.github.io/sme-tools)
[![DPIIT Registered](https://img.shields.io/badge/Venture-DPIIT%20Registered-blue?style=flat-square)](https://muskanchallana.vercel.app)

**[🚀 Live Demo](https://crm-template.streamlit.app)** · **[Landing Page](https://challanamuskan.github.io/sme-tools)** · **[Builder Portfolio](https://muskanchallana.vercel.app)**

Demo login: `admin` / `demo123`

---

## 🇮🇳 Why This Exists

63 million Indian SMEs run on paper registers, WhatsApp threads, and Excel files. Most can't afford ₹5,000/month SaaS. This platform gives them a **complete digital business OS** — CRM, marketing, finance, supply chain, content, and global reach — deployable in under 30 minutes, free to self-host.

**Built from a live production deployment** serving a 30-year-old textile machinery business in Jaipur — 2000+ products, real orders, real customers. Client data removed. All logic preserved and expanded.

---

## 🚀 What's Inside: 8 Growth Pillars

### 1. 📊 CRM & Customer Management
Full customer lifecycle — leads, orders, payments, follow-ups, WhatsApp integration.

| Module | What It Does |
|--------|-------------|
| 📦 **Stock Tracker** | Live inventory, low-stock alerts, bulk import, value-by-category charts |
| 👥 **Customer CRM** | Profiles, purchase history, payment health, lifecycle stage |
| 💰 **GST Invoices** | GST-compliant PDF invoice generator (CGST/SGST/IGST auto-split) |
| 📱 **WhatsApp Orders** | Upload chat export → auto-extract orders, amounts, customer names |
| 📧 **Email Tracker** | Gmail compose shortcuts, templates, follow-up log with urgency flags |

---

### 2. 📣 Marketing & Growth
Multi-channel marketing tools built for Indian SME budgets and platforms.

| Module | What It Does |
|--------|-------------|
| 🎯 **Promotions Engine** | WhatsApp broadcast links, offer builder, Indian seasonal campaign calendar |
| 📣 **Ad Tracker** | Campaign log, budget vs spend, ROI per channel (WhatsApp / Instagram / Google / JustDial) |
| 🌐 **Website Manager** | Uptime monitor, web leads capture, SEO checklist, analytics embed |
| 📊 **Business Intelligence** | Revenue trends, payment health, stock value, campaign ROI charts |

---

### 3. ⚖️ Finance & Accounting
GST, TDS, compliance — the Indian finance stack.

| Module | What It Does |
|--------|-------------|
| ⚖️ **Compliance Calendar** | GSTR-1, GSTR-3B, TDS deadlines, e-Way bill checker, GST rate finder |
| 🧾 **GST Invoices** | Auto-compute CGST/SGST/IGST, PDF download, invoice history |
| 💳 **Payment Tracker** | UPI, bank transfer, cash — payment status, overdue alerts |
| 📈 **P&L Dashboard** | Monthly revenue, cost, margin view — no accountant needed for basics |

---

### 4. 🚚 Supply Chain & Inventory
End-to-end from supplier to customer.

| Module | What It Does |
|--------|-------------|
| 📦 **Stock Tracker** | Real-time inventory, supplier mapping, reorder alerts |
| 🚚 **e-Way Bill Checker** | Instant ₹50K threshold check, link to NIC portal |
| 🏭 **Supplier Manager** | Supplier contacts, purchase history, lead time tracking |
| 📋 **Purchase Orders** | PO creation, receiving, supplier payment tracking |

---

### 5. 📝 Content & Communication
Generate, track, and schedule business content.

| Module | What It Does |
|--------|-------------|
| 📝 **WhatsApp Templates** | Reusable message templates for orders, reminders, offers |
| 📧 **Email Templates** | Payment reminder, order confirmation, custom — Gmail shortcut links |
| 🎁 **Offer Builder** | Generate festival offer messages (Diwali, Holi, Eid, etc.) |
| 📅 **Seasonal Calendar** | 12-month Indian business event calendar with opportunity tags |

---

### 6. 🌏 Global Connection & Export
Tools for Indian SMEs expanding internationally.

| Module | What It Does |
|--------|-------------|
| 💱 **Currency Converter** | Live INR↔USD/EUR/AED/GBP rates for export invoicing |
| 🌐 **Export Compliance Checklist** | IEC code, AD Code, DGFT, shipping bill basics |
| 🤝 **IndiaMart / TradeIndia Integration** | Lead import from B2B portals into CRM |
| 📦 **International Shipment Tracker** | Track shipments via courier API |

---

### 7. 🔔 AI-Powered Intelligence
Smart layer on top of all modules.

| Module | What It Does |
|--------|-------------|
| 🔔 **Smart Reminders** | AI-generated action items from live data: overdue payments, reorder, compliance |
| 🏥 **Business Health Score** | 0–100 score across payments, stock, compliance, marketing |
| 📊 **BI Dashboard** | Revenue trends, top customers, best products, payment health |
| 🤖 **AI Insights** | Natural language summaries of your business performance |

---

### 8. 🏢 Operations & Staff
Run the back office without an office manager.

| Module | What It Does |
|--------|-------------|
| 🏢 **MIS & Staff** | Attendance log, task assignment, role management |
| 🔐 **Role-Based Auth** | Admin / Staff / Viewer access — Streamlit secrets-based |
| ⚙️ **Config YAML** | Single file to customise business name, GSTIN, currency, features |

---

## ⚡ Deploy in 5 Minutes

### 1. Fork this repo

### 2. Create free Supabase project
```
supabase.com → New Project → copy URL + anon key
```
Run `sample_data/seed.sql` in Supabase SQL Editor → all tables + demo data created.

### 3. Configure your business
Edit `config.yaml`:
```yaml
business:
  name: "Sharma Textile Traders"
  gstin: "08ABCDE1234F1Z5"
  currency: "₹"
  state: "Rajasthan"
```

### 4. Deploy to Streamlit Cloud
```
streamlit.io/cloud → New App → connect repo → main file: app.py
```
Add secrets:
```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_KEY = "your-anon-key"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "yourpassword"
```

Done. Your business OS is live. ✅

---

## 🗂️ Project Structure

```
indian-sme-crm-template/
├── app.py                          # Entry point + auth + home dashboard
├── config.yaml                     # Business config (name, GSTIN, features)
├── pages/
│   ├── 06_GST_Invoices.py          # GST-compliant PDF invoices
│   ├── 07_Customers.py             # Customer CRM
│   ├── 08_Ad_Tracker.py            # Campaign + ROI tracker
│   ├── 09_Website_Analytics.py     # Analytics embed
│   ├── 10_Compliance.py            # GSTR/TDS deadlines + e-Way + GST rates
│   ├── 11_Business_Intelligence.py # BI charts
│   ├── 12_WhatsApp_Orders.py       # Chat export parser
│   ├── 13_Smart_Reminders.py       # AI reminders + health score
│   ├── 14_Stock_Tracker.py         # Live inventory
│   ├── 15_Email_Tracker.py         # Email templates + follow-up log
│   ├── 16_Website_Manager.py       # Uptime + SEO + leads
│   ├── 17_Promotions.py            # Broadcast + offer builder
│   ├── 18_Supply_Chain.py          # Suppliers + POs + e-Way
│   ├── 19_Finance_PL.py            # P&L dashboard
│   ├── 20_Content_Hub.py           # Templates + seasonal calendar
│   └── 21_Global_Export.py         # Currency + export tools
├── utils/
│   ├── auth.py                     # Role-based auth
│   ├── db.py                       # Supabase abstraction
│   ├── config_loader.py
│   ├── invoice_gen.py              # GST PDF invoice (ReportLab)
│   └── notifications.py            # Gmail + WhatsApp
├── sample_data/
│   └── seed.sql                    # All tables + demo retail data
├── .streamlit/
│   └── secrets.toml.example
├── requirements.txt
└── docs/
    ├── deploy.md
    ├── gmail_setup.md
    └── modules.md
```

---

## 🛠 Tech Stack

`Python 3.11` · `Streamlit` · `Supabase (PostgreSQL)` · `Pandas` · `Plotly` · `ReportLab` · `Gmail API` · `WhatsApp Web`

---

## 🏭 Who This Is For

| Business Type | Key Modules |
|--------------|-------------|
| **Textile / Manufacturing** | Stock, GST Invoices, Compliance, WhatsApp Orders |
| **Retail / Wholesale** | CRM, Promotions, Ad Tracker, Payment Tracker |
| **Trading / Export** | Supply Chain, Global Export, Finance P&L |
| **Services / Consulting** | Email Tracker, CRM, Business Intelligence |
| **HNI Portfolio Businesses** | BI Dashboard, P&L, Multi-location Stock |

---

## 📊 Real Impact

> "This CRM saves our team **significant hours every week** — WhatsApp order entry alone used to take 2 hours daily."
> — Live client, textile machinery business, Jaipur (2000+ products, active deployment)

---

## 🤝 Part of SME Tools

- 🏪 **[indian-sme-crm-template](https://github.com/challanamuskan/indian-sme-crm-template)** ← you are here
- 📬 **[sme-inbox-parser](https://github.com/challanamuskan/sme-inbox-parser)** — WhatsApp + Gmail + website leads → CSV
- 📋 **[awesome-indian-sme-tools](https://github.com/challanamuskan/awesome-indian-sme-tools)** — curated toolkit for Indian SME builders

---

## 📄 License

MIT — free for commercial use.

*Built with ❤️ for Indian SMEs. Star ⭐ if this saved you time.*
