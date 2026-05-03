# 🏪 Indian SME & HNI Growth Platform

> From CRM to full business OS — built for Indian small businesses, growing enterprises, and high-net-worth clients who want AI-powered growth tools without enterprise pricing.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-crm--template.streamlit.app-FF4B4B?style=flat-square&logo=streamlit)](https://crm-template.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Supabase](https://img.shields.io/badge/Database-Supabase-3ECF8E?style=flat-square&logo=supabase)](https://supabase.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Built for India](https://img.shields.io/badge/Built%20for-Indian%20SMEs%20🇮🇳-orange?style=flat-square)](https://challanamuskan.github.io/sme-tools)
[![DPIIT Registered](https://img.shields.io/badge/Venture-DPIIT%20Registered-blue?style=flat-square)](https://muskanchallana.vercel.app)

**[🚀 Live Demo](https://crm-template.streamlit.app)** · **[Landing Page](https://challanamuskan.github.io/sme-tools)** · **[Builder Portfolio](https://muskanchallana.vercel.app)**

---

## 🇮🇳 Why This Exists

63 million Indian SMEs run on paper registers, WhatsApp threads, and Excel files. Most can't afford ₹5,000/month SaaS. This platform gives them a **complete digital business OS** — CRM, marketing, finance, supply chain, content, and global reach — deployable in under 30 minutes, free to self-host.

**Built from a live production deployment** serving a 30-year-old textile machinery business in Jaipur — 2000+ products, real orders, real customers. Saves the client **12 hours/week**.

---

## 🚀 What's Inside: 8 Growth Pillars

### 1. 📊 CRM & Customer Management
Full customer lifecycle — leads, orders, payments, follow-ups, WhatsApp integration.

### 2. 📣 Marketing & Growth
Campaign tracker with ROI, monthly growth KPIs, content calendar, 8 message templates, customer segmentation (Champions / Loyal / At Risk / Lost).

### 3. 💰 Finance & Accounting
P&L dashboard, transaction ledger, accounts payable/receivable, GST summary (output vs input tax), cumulative cashflow chart.

### 4. 🌐 Global Supply Chain & Inventory
Industry trade map (8 industries) — finds global buyers + suppliers simultaneously. Dual-level inventory: raw materials + finished goods. Self-marketing pitch generator. Export market map.

### 5. 📦 Stock & Operations
Live inventory, reorder alerts, supplier mapping, e-Way bill checker.

### 6. ⚖️ GST & Compliance
GSTR-1/3B/TDS deadlines, e-Way bill checker, GST rate finder, advance tax calendar.

### 7. 🔔 AI Intelligence
Smart reminders from live data, business health score, BI dashboard.

### 8. 🏢 Staff & Access Control
Role-based auth, 7 temp client demo accounts with usage limits, admin reset panel.

---

## ⚡ Deploy in 5 Minutes

### 1. Fork this repo

### 2. Create free Supabase project
Go to [supabase.com](https://supabase.com) → New Project → copy URL + anon key.

Run `sample_data/seed.sql` in Supabase SQL Editor, then run `demo_usage_migration.sql` to enable demo account tracking.

### 3. Configure your business
Edit `config.yaml`:
```yaml
business:
  name: "Your Business Name"
  gstin: "08ABCDE1234F1Z5"
  currency: "₹"
  state: "Rajasthan"
```

### 4. Deploy to Streamlit Cloud
Go to [share.streamlit.io](https://share.streamlit.io) → New App → connect repo → main file: `app.py`.

Set all credentials in **Streamlit Cloud → App Settings → Secrets** (see `secrets.toml.example`).

### 5. Inject auth guard into all pages (run once locally)
```bash
python patch_auth.py
git add -A && git commit -m "security: auth guard all pages" && git push
```

---

## 🗂️ Project Structure

```
indian-sme-crm-template/
├── app.py                           # Entry point + auth + home dashboard
├── config.yaml                      # Business config
├── patch_auth.py                    # One-time: injects login guard into all pages
├── demo_usage_migration.sql         # Supabase migration for demo account tracking
├── pages/
│   ├── 06_GST_Invoices.py
│   ├── 08_Ad_Tracker.py
│   ├── 09_Website_Analytics.py
│   ├── 10_Compliance.py
│   ├── 11_Business_Intelligence.py
│   ├── 12_WhatsApp_Orders.py
│   ├── 13_Smart_Reminders.py
│   ├── 14_Stock_Tracker.py
│   ├── 15_Email_Tracker.py
│   ├── 16_Website_Manager.py
│   ├── 17_Promotions.py
│   ├── 18_Supply_Chain_Global.py    # ★ Global buyers/suppliers + dual inventory
│   ├── 19_Finance_Accounting.py     # ★ P&L + GST + cashflow
│   ├── 20_Marketing_Growth.py       # ★ Campaigns + growth metrics + content
│   └── 21_Admin_Panel.py            # ★ Demo account manager (admin only)
├── utils/
│   ├── auth.py                      # Auth + temp demo accounts (Supabase-persisted)
│   ├── auth_guard.py                # Single-import login guard for pages
│   ├── db.py
│   ├── config_loader.py
│   ├── invoice_gen.py
│   └── notifications.py
├── sample_data/
│   └── seed.sql
└── .streamlit/
    └── secrets.toml.example
```

---

## 🛠 Tech Stack

`Python 3.11` · `Streamlit` · `Supabase (PostgreSQL)` · `Pandas` · `Plotly` · `ReportLab` · `Gmail API` · `WhatsApp Web`

---

## 📊 Real Impact

> Client saves **12 hours/week** — WhatsApp order entry alone used to take 2 hours daily.
> — Live deployment, textile machinery business, Jaipur (2000+ products)

---

## 🤝 Part of SME Tools

- 🏪 **[indian-sme-crm-template](https://github.com/challanamuskan/indian-sme-crm-template)** ← you are here
- 📬 **[sme-inbox-parser](https://github.com/challanamuskan/sme-inbox-parser)**
- 📋 **[awesome-indian-sme-tools](https://github.com/challanamuskan/awesome-indian-sme-tools)**

---

## 📄 License

MIT — free for commercial use.

*Built with ❤️ for Indian SMEs. Star ⭐ if this saved you time.*
