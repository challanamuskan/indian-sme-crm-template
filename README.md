# Indian SME CRM Template

> Open-source CRM template for Indian small businesses — stock, sales, payments, WhatsApp alerts, and employee management in one Streamlit app.

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Sheets](https://img.shields.io/badge/Google_Sheets-34A853?style=flat-square&logo=google-sheets&logoColor=white)](https://developers.google.com/sheets)
[![Gmail API](https://img.shields.io/badge/Gmail_API-EA4335?style=flat-square&logo=gmail&logoColor=white)](https://developers.google.com/gmail)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen?style=flat-square)](https://satyam-tex-fabb.streamlit.app)

**[🌐 Live Demo](https://satyam-tex-fabb.streamlit.app)** · **[Builder Portfolio](https://muskanchallana.vercel.app)**

---

## What This Is

Production-ready CRM template for Indian SMEs still running on Tally + WhatsApp. Fork it, swap the Google Sheet IDs, deploy to Streamlit Cloud — working CRM in hours.

**Proof point:** Live at [Satyam Tex Fabb](https://satyam-tex-fabb.streamlit.app), a 30-year textile machinery parts dealer in Bhilwara, Rajasthan. Manages 2,000+ SKUs across multiple suppliers, replaces fragmented Tally records and WhatsApp order threads.

---

## Features

- **Stock Manager** — Category → Part → Supplier hierarchy; multi-supplier price tracking; full price history forever
- **Sales & Purchases** — Record transactions with bill upload; stock auto-adjusts on every entry; returns supported
- **Payments & Reminders** — Overdue highlights; automated email + WhatsApp payment reminders and purchase orders
- **OCR Bill Scanning** — Upload bill photo; pytesseract + pdfplumber auto-fills form fields
- **MIS Dashboard** — Daily task assignment, employee attendance, performance analytics
- **Bulk Import** — Chunked 400-row batch with progress bar; XLS/XLSX/CSV supported; Tally-compatible export

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Language | Python 3.9+ |
| Database | Google Sheets (gspread) |
| Email | Gmail API (OAuth2) |
| WhatsApp | Click-to-chat links |
| OCR | pytesseract + pdfplumber |
| Export | openpyxl + xlsxwriter |
| Auth | SHA-256 hashing, role-based access |
| Deployment | Streamlit Community Cloud |

---

## Live Demo

**[satyam-tex-fabb.streamlit.app](https://satyam-tex-fabb.streamlit.app)** — live deployment for Satyam Tex Fabb, Bhilwara, Rajasthan

---

## Key Results

- Replaced Tally + WhatsApp chaos for a 30-year textile parts business
- 2,000+ SKUs tracked in real time across multiple suppliers
- Automated low-stock alerts on 1st and 15th of each month — no manual checking
- OCR scanning cuts manual bill entry time significantly
- Field staff attendance and daily tasks logged from one dashboard

---

## Quick Start

```bash
git clone https://github.com/challanamuskan/indian-sme-crm-template
cd indian-sme-crm-template
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Add credentials to project root: Google service account JSON + Gmail OAuth JSON.

Set admin email in `.streamlit/secrets.toml`:
```toml
admin_email = "your-gmail-address"
```

```bash
streamlit run app.py
```

---

## Related

- **[shree-tex-fabb-crm](https://github.com/challanamuskan/shree-tex-fabb-crm)** — Production v2 with Supabase PostgreSQL backend and image catalogue
- **[sme-inbox-parser](https://github.com/challanamuskan/sme-inbox-parser)** — Parse WhatsApp + Gmail + website leads into CRM-ready CSV
- **[awesome-indian-sme-tools](https://github.com/challanamuskan/awesome-indian-sme-tools)** — Curated toolkit for Indian SME software builders

---

[Portfolio](https://muskanchallana.vercel.app) · [LinkedIn](https://www.linkedin.com/in/muskan-challana-408234213/) · [Email](mailto:cmuskan2068@gmail.com) · [GitHub](https://github.com/challanamuskan)
