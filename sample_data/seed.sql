-- ─────────────────────────────────────────────────────────────
--  Indian SME CRM Template — Database Schema + Demo Seed Data
--  Run this in Supabase SQL Editor → click Run
-- ─────────────────────────────────────────────────────────────

-- Products / Inventory
CREATE TABLE IF NOT EXISTS products (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    category    TEXT,
    hsn_code    TEXT,
    quantity    INTEGER DEFAULT 0,
    unit        TEXT DEFAULT 'pcs',
    price       NUMERIC(12,2) DEFAULT 0,
    supplier    TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Customers
CREATE TABLE IF NOT EXISTS customers (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    phone       TEXT,
    email       TEXT,
    address     TEXT,
    gstin       TEXT,
    stage       TEXT DEFAULT 'active',
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Sales
CREATE TABLE IF NOT EXISTS sales (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    date        DATE DEFAULT CURRENT_DATE,
    total       NUMERIC(12,2),
    discount    NUMERIC(5,2) DEFAULT 0,
    status      TEXT DEFAULT 'completed',
    notes       TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Sale items
CREATE TABLE IF NOT EXISTS sale_items (
    id          SERIAL PRIMARY KEY,
    sale_id     INTEGER REFERENCES sales(id) ON DELETE CASCADE,
    product_id  INTEGER REFERENCES products(id),
    quantity    NUMERIC(10,2),
    unit_price  NUMERIC(12,2),
    total       NUMERIC(12,2)
);

-- Purchases
CREATE TABLE IF NOT EXISTS purchases (
    id          SERIAL PRIMARY KEY,
    supplier    TEXT,
    date        DATE DEFAULT CURRENT_DATE,
    total       NUMERIC(12,2),
    status      TEXT DEFAULT 'received',
    invoice_ref TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Payments
CREATE TABLE IF NOT EXISTS payments (
    id          SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    amount      NUMERIC(12,2),
    method      TEXT,
    reference   TEXT,
    status      TEXT DEFAULT 'completed',
    due_date    DATE,
    notes       TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Campaigns / Ad tracker
CREATE TABLE IF NOT EXISTS campaigns (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    channel     TEXT,
    budget      NUMERIC(12,2),
    spend       NUMERIC(12,2) DEFAULT 0,
    leads       INTEGER DEFAULT 0,
    conversions INTEGER DEFAULT 0,
    goal        TEXT,
    start_date  DATE,
    end_date    DATE,
    notes       TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);

-- Staff
CREATE TABLE IF NOT EXISTS staff (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    role        TEXT DEFAULT 'staff',
    phone       TEXT,
    email       TEXT,
    active      BOOLEAN DEFAULT TRUE
);

-- ─────────────────────────────────────────────────────────────
--  DEMO SEED DATA — Generic Retail Shop
-- ─────────────────────────────────────────────────────────────

INSERT INTO products (name, category, hsn_code, quantity, unit, price, supplier) VALUES
    ('Bearing Set 6205',    'Bearings',   '8482', 150, 'pcs',  250.00, 'Rajasthan Bearings Co'),
    ('Flat Pulley 6 inch',  'Pulleys',    '8483', 42,  'pcs',  320.00, 'Jaipur Hardware'),
    ('Industrial Belt B-38','Belts',      '4010', 8,   'pcs',  180.00, 'Rajasthan Bearings Co'),
    ('Cotton Fabric White', 'Fabric',     '5208', 200, 'mtr',  185.00, 'Textile Suppliers'),
    ('Cotton Fabric Blue',  'Fabric',     '5208', 6,   'mtr',  195.00, 'Textile Suppliers'),
    ('Motor 0.5HP',         'Motors',     '8501', 25,  'pcs', 2800.00, 'Electric Parts Depot'),
    ('Shaft 25mm',          'Shafts',     '7326', 60,  'pcs',  420.00, 'Jaipur Hardware'),
    ('Gear Box Type A',     'Gear Boxes', '8483', 4,   'pcs', 3500.00, 'Rajasthan Bearings Co');

INSERT INTO customers (name, phone, email, address) VALUES
    ('Ramesh Traders',     '+919876543210', 'ramesh@example.com',  'Shop 12, Sindhi Camp, Jaipur'),
    ('Priya Stores',       '+919876543211', 'priya@example.com',   'MI Road, Jaipur'),
    ('Kumar and Co',       '+919876543212', 'kumar@example.com',   'Sanganer, Jaipur'),
    ('Sharma Hardware',    '+919876543213', 'sharma@example.com',  'Bani Park, Jaipur'),
    ('Singh Enterprises',  '+919876543214', 'singh@example.com',   'Malviya Nagar, Jaipur');

INSERT INTO sales (customer_id, date, total, status) VALUES
    (1, CURRENT_DATE,       12500.00, 'completed'),
    (2, CURRENT_DATE - 1,    9000.00, 'completed'),
    (3, CURRENT_DATE - 2,    6750.00, 'completed'),
    (4, CURRENT_DATE - 3,    4200.00, 'completed'),
    (5, CURRENT_DATE - 5,   15600.00, 'completed'),
    (1, CURRENT_DATE - 7,    8400.00, 'completed'),
    (2, CURRENT_DATE - 10,  11200.00, 'completed');

INSERT INTO payments (customer_id, amount, method, status, due_date) VALUES
    (1, 12500.00, 'UPI',           'completed', CURRENT_DATE),
    (2,  9000.00, 'Bank Transfer', 'pending',   CURRENT_DATE + 3),
    (3,  6750.00, 'Cash',          'completed', CURRENT_DATE - 2),
    (4,  4200.00, 'UPI',           'pending',   CURRENT_DATE - 5),
    (5, 15600.00, 'Bank Transfer', 'completed', CURRENT_DATE - 5);

INSERT INTO campaigns (name, channel, budget, spend, leads, conversions, goal, start_date, end_date) VALUES
    ('April WhatsApp Blast', 'WhatsApp Broadcast', 2000,  1800, 45, 12, 'Sales',            CURRENT_DATE - 14, CURRENT_DATE),
    ('Instagram Spring Sale','Instagram',          5000,  3200, 89, 18, 'Brand Awareness',  CURRENT_DATE - 10, CURRENT_DATE + 5),
    ('Google Ads - Bearings','Google Ads',         8000,  6100, 124, 31, 'Lead Generation', CURRENT_DATE - 7,  CURRENT_DATE + 7);

INSERT INTO staff (name, role, phone) VALUES
    ('Amit Verma',   'admin', '+919800000001'),
    ('Pooja Singh',  'staff', '+919800000002'),
    ('Rahul Sharma', 'staff', '+919800000003');
