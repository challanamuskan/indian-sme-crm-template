# 🚀 Deploy Guide — Indian SME CRM Template

## Prerequisites
- GitHub account
- Supabase account (free tier works)
- Streamlit Community Cloud account (free)

---

## Step 1 — Fork the repo
Click **Fork** on GitHub → your account.

## Step 2 — Set up Supabase

1. Create project at [supabase.com](https://supabase.com)
2. Go to **SQL Editor** → paste and run `schema.sql` (in this repo)
3. Copy: **Project URL** and **Anon public key** from Settings → API

## Step 3 — Configure your business

Edit `config.yaml`:
```yaml
business:
  name: "Sharma Hardware Store"
  gstin: "08AAAAA0000A1Z5"
  city: "Jaipur"
  ...
```

## Step 4 — Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app** → connect your forked repo
3. Main file: `app.py`
4. Click **Advanced settings** → paste secrets:

```toml
SUPABASE_URL = "https://xxxx.supabase.co"
SUPABASE_ANON_KEY = "your-key"

[users.admin]
password_hash = "your-sha256-hash"
role = "admin"
```

5. Click **Deploy** ✅

## Your CRM is live in ~2 minutes.

---

## Optional: Custom Domain
Streamlit Cloud supports custom subdomains on Pro plan.
For full custom domain → deploy to Railway or Render instead.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `SUPABASE_URL not found` | Check secrets.toml formatting |
| `relation does not exist` | Run schema.sql in Supabase SQL Editor |
| `reportlab not installed` | Add to requirements.txt (already included) |
