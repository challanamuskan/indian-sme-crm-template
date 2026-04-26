# 🏪 Indian SME CRM Template

> A production-ready, plug-and-play CRM built for Indian small & medium businesses. Configure once, deploy in minutes.

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Supabase](https://img.shields.io/badge/Backend-Supabase-green)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Made for India](https://img.shields.io/badge/Made%20for-Indian%20SMEs-orange)](https://github.com/challanamuskan)

---

## ✨ What This Is

Most Indian SMBs run their business on WhatsApp + Excel. This template gives them a real CRM — inventory, sales, customers, GST invoices, compliance reminders, and ad tracking — deployed on the cloud in under 10 minutes, for free.

Built from a **live production deployment** serving a textile machinery parts business in Rajasthan. All client data removed. All logic preserved.

---

## 🚀 Features

| Module | What It Does |
|--------|-------------|
| 📦 **Stock Manager** | Inventory with multi-supplier price tracking, low-stock alerts, category navigation |
| 💰 **Sales & Purchases** | Full order lifecycle, multi-product entries, return tracking |
| 👥 **Customers & Leads** | Contact book, lead pipeline, communication log |
| 💳 **Payments** | Payment tracking, due date alerts, payment history per customer |
| 🧾 **GST Invoice Generator** | Auto-filled GST invoices with your GSTIN, PDF export |
| 📋 **Order Lists & POs** | Purchase orders, delivery challan generation |
| 📣 **Ad & Promotion Tracker** | Campaign budget, reach, ROI — track every rupee spent on marketing |
| 🌐 **Website Analytics** | Embed your Plausible/Umami/GA dashboard, track visitors per campaign |
| ⚖️ **Govt Compliance** | GST filing reminders, TDS deadlines, MSME registration tracker |
| 👔 **MIS & Staff** | Employee attendance, daily task assignment, performance log |
| 📊 **Analytics** | Revenue trends, top products, customer spend heatmap, 7 live charts |
| 📧 **Notifications** | Gmail payment reminders + WhatsApp click-to-chat (configurable) |

---

## ⚡ Deploy in 5 Minutes

### 1. Fork this repo

### 2. Set up Supabase
- Create free project at [supabase.com](https://supabase.com)
- Copy your `SUPABASE_URL` and `SUPABASE_ANON_KEY`

### 3. Configure your business
Edit `config.yaml`:
```yaml
business:
  name: "Your Business Name"
  tagline: "Your tagline here"
  gstin: "YOUR_GSTIN_HERE"
  currency: "₹"
  logo_url: ""            # optional: paste image URL
  city: "Jaipur"
  state: "Rajasthan"
  phone: "+91-XXXXXXXXXX"
  email: "you@yourbusiness.com"

features:
  whatsapp_enabled: true
  gmail_enabled: false    # requires Gmail API setup (see docs/gmail_setup.md)
  website_analytics_url: ""  # paste your Plausible/Umami URL
```

### 4. Deploy to Streamlit Cloud
- Push to your GitHub
- Go to [share.streamlit.io](https://share.streamlit.io)
- Connect repo → set secrets (see `.streamlit/secrets.toml.example`)
- Deploy ✅

**Full guide:** [docs/deploy.md](docs/deploy.md)

---

## 🔧 Tech Stack

- **Frontend:** Streamlit (Python)
- **Database:** Supabase (PostgreSQL)
- **Auth:** SHA-256 hashed, role-based (Admin / Staff)
- **PDF:** ReportLab (invoices, challans)
- **Notifications:** Gmail API + WhatsApp Web click-to-chat
- **Charts:** Plotly

---

## 📁 Project Structure

```
indian-sme-crm-template/
├── app.py                    # Entry point
├── config.yaml               # ← Your business config here
├── pages/
│   ├── 1_Stock_Manager.py
│   ├── 2_Sales.py
│   ├── 3_Purchases.py
│   ├── 4_Customers.py
│   ├── 5_Payments.py
│   ├── 6_GST_Invoices.py
│   ├── 7_Order_Lists.py
│   ├── 8_Ad_Tracker.py
│   ├── 9_Website_Analytics.py
│   ├── 10_Compliance.py
│   ├── 11_MIS.py
│   └── 12_Analytics.py
├── utils/
│   ├── db.py                 # Supabase wrapper
│   ├── auth.py               # Login, session, roles
│   ├── invoice_gen.py        # GST invoice PDF engine
│   ├── notifications.py      # Gmail + WhatsApp
│   └── config_loader.py      # Reads config.yaml
├── .streamlit/
│   └── secrets.toml.example
├── docs/
│   ├── deploy.md
│   └── gmail_setup.md
└── requirements.txt
```

---

## 🇮🇳 Who This Is For

- Textile / garment traders
- Hardware & machinery parts dealers  
- Wholesale distributors
- Any Indian SME currently managing business on WhatsApp + Excel

---

## 🛠 Built By

[Muskan Challana](https://muskanchallana.vercel.app) — Freelance AI & CRM Builder, MCA @ VGU Jaipur  
Deployed this in production for a live client in Rajasthan. Open-sourced the template for Indian SME builders.

> 💡 Need a custom version for your business? [Get in touch](https://muskanchallana.vercel.app)

---

## 📄 License

MIT — use freely, credit appreciated.
