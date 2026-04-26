# 🏪 Indian SME CRM Template

> Production-ready, plug-and-play CRM built for Indian small & medium businesses — textile, retail, wholesale, manufacturing, and beyond.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-crm--template.streamlit.app-FF4B4B?style=flat-square&logo=streamlit)](https://crm-template.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat-square&logo=supabase)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Built for India](https://img.shields.io/badge/Built%20for-Indian%20SMEs%20🇮🇳-orange?style=flat-square)](https://challanamuskan.github.io/sme-tools)

**[🚀 Live Demo](https://crm-template.streamlit.app)** · **[Landing Page](https://challanamuskan.github.io/sme-tools)** · **[Builder Portfolio](https://muskanchallana.vercel.app)**

Login: `admin` / `demo123`

---

## ✨ What This Does

Most Indian SMEs manage their entire business on WhatsApp threads and paper registers. This template gives them a full digital CRM in under 30 minutes — no developers needed after setup.

**Built from a live production deployment** serving a 30-year-old textile machinery business in Jaipur — 2000+ products, real orders, real customers. All client data removed. All logic preserved.

---

## 🚀 11 Modules

| Module | What It Does |
|--------|-------------|
| 📦 **Stock Tracker** | Live inventory, low-stock alerts, category charts, bulk import |
| 💰 **GST Invoices** | GST-compliant PDF invoice generator (CGST/SGST/IGST) |
| 📣 **Ad Tracker** | Campaign log, budget vs spend, ROI per channel |
| 🌐 **Website Manager** | Uptime monitor, web leads capture, SEO checklist, analytics embed |
| ⚖️ **Compliance Calendar** | GSTR-1, GSTR-3B, TDS deadlines + e-Way bill checker + GST rate finder |
| 📊 **Business Intelligence** | Revenue trends, payment health, stock value, campaign ROI |
| 📱 **WhatsApp Orders** | Upload chat export → auto-extract orders, amounts, customers |
| 🔔 **Smart Reminders** | AI-generated action items + Business Health Score (0–100) |
| 🎯 **Promotions** | WhatsApp broadcast links, offer builder, Indian seasonal calendar |
| 📧 **Email Tracker** | Gmail compose shortcuts, templates, follow-up log with urgency flags |
| 🏢 **MIS & Staff** | Attendance log, task assignment, role management |

---

## ⚡ Deploy in 5 Minutes

### 1. Fork this repo

### 2. Create free Supabase project
```
supabase.com → New Project → copy URL + anon key
```
Run `sample_data/seed.sql` in Supabase SQL Editor to create all tables + demo data.

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

---

## 🗂️ Project Structure

```
indian-sme-crm-template/
├── app.py                         # Entry point + auth + home dashboard
├── config.yaml                    # Business config (name, GSTIN, features)
├── pages/
│   ├── 6_GST_Invoices.py
│   ├── 8_Ad_Tracker.py
│   ├── 9_Website_Analytics.py
│   ├── 10_Compliance.py           # Fixed: safe dates + e-Way bill + GST rate finder
│   ├── 11_Business_Intelligence.py
│   ├── 12_WhatsApp_Orders.py      # Working WhatsApp chat parser
│   ├── 13_Smart_Reminders.py      # AI reminders + health score
│   ├── 14_Stock_Tracker.py
│   ├── 15_Email_Tracker.py
│   ├── 16_Website_Manager.py
│   └── 17_Promotions.py
├── utils/
│   ├── auth.py                    # Role-based auth (Admin/Staff/Viewer)
│   ├── db.py                      # Supabase abstraction layer
│   ├── config_loader.py
│   ├── invoice_gen.py             # GST PDF invoice (interface stub)
│   └── notifications.py           # Gmail + WhatsApp (interface stub)
├── sample_data/
│   └── seed.sql                   # All tables + demo retail shop data
├── .streamlit/
│   └── secrets.toml.example
├── requirements.txt
└── deploy.md
```

---

## 🛠 Tech Stack

`Python 3.11` · `Streamlit` · `Supabase (PostgreSQL)` · `Pandas` · `Plotly` · `ReportLab` · `Gmail API` · `WhatsApp Web`

---

## 🤝 Part of SME Tools

This repo is part of the **[SME Tools](https://challanamuskan.github.io/sme-tools)** open-source suite for Indian businesses:

- 🏪 **[indian-sme-crm-template](https://github.com/challanamuskan/indian-sme-crm-template)** ← you are here
- 📬 **[sme-inbox-parser](https://github.com/challanamuskan/sme-inbox-parser)** — WhatsApp + Gmail + website leads → CSV
- 📋 **[awesome-indian-sme-tools](https://github.com/challanamuskan/awesome-indian-sme-tools)** — curated toolkit

---

## 📄 License

MIT — free for commercial use.

*Built with ❤️ for Indian SMEs. If this saved you time, star ⭐ the repo.*
