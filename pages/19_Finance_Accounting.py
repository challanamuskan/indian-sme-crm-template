import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
import calendar

st.set_page_config(page_title="💰 Finance & Accounting", layout="wide")

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("🔒 Please login first")
    st.stop()

# ─── Session State Init ────────────────────────────────────────
def init_finance():
    if "transactions" not in st.session_state:
        st.session_state.transactions = pd.DataFrame([
            {"Date": "2026-04-01", "Type": "Income", "Category": "Sales",
             "Description": "Fabric sale – Rajan Textiles", "Amount": 45000.0,
             "Tax_GST": 8100.0, "Payment_Mode": "Bank Transfer", "Reference": "INV-001"},
            {"Date": "2026-04-03", "Type": "Expense", "Category": "Raw Material",
             "Description": "Cotton yarn purchase", "Amount": 28000.0,
             "Tax_GST": 5040.0, "Payment_Mode": "Cheque", "Reference": "PO-2024"},
            {"Date": "2026-04-07", "Type": "Income", "Category": "Sales",
             "Description": "Export shipment – UAE buyer", "Amount": 182000.0,
             "Tax_GST": 0.0, "Payment_Mode": "Wire Transfer", "Reference": "EXP-007"},
            {"Date": "2026-04-10", "Type": "Expense", "Category": "Operations",
             "Description": "Electricity bill", "Amount": 12500.0,
             "Tax_GST": 2250.0, "Payment_Mode": "Online", "Reference": "UTIL-04"},
            {"Date": "2026-04-15", "Type": "Expense", "Category": "Salaries",
             "Description": "Staff salaries – April 1-15", "Amount": 65000.0,
             "Tax_GST": 0.0, "Payment_Mode": "Bank Transfer", "Reference": "PAY-15"},
            {"Date": "2026-04-20", "Type": "Income", "Category": "Services",
             "Description": "CRM setup fee – new client", "Amount": 35000.0,
             "Tax_GST": 6300.0, "Payment_Mode": "UPI", "Reference": "SVC-003"},
        ])
    if "payables" not in st.session_state:
        st.session_state.payables = pd.DataFrame([
            {"Vendor": "Vardhman Mills", "Invoice_No": "VM-445", "Amount": 48000.0,
             "Due_Date": "2026-05-10", "Status": "Pending", "Category": "Raw Material"},
            {"Vendor": "Sharma Logistics", "Invoice_No": "SL-89", "Amount": 8500.0,
             "Due_Date": "2026-05-05", "Status": "Overdue", "Category": "Freight"},
        ])
    if "receivables" not in st.session_state:
        st.session_state.receivables = pd.DataFrame([
            {"Customer": "Rajan Textiles", "Invoice_No": "INV-001", "Amount": 53100.0,
             "Due_Date": "2026-05-01", "Status": "Partial", "Paid": 25000.0},
            {"Customer": "UAE Buyer Co.", "Invoice_No": "EXP-007", "Amount": 182000.0,
             "Due_Date": "2026-05-15", "Status": "Pending", "Paid": 0.0},
        ])

init_finance()

# ─── Helpers ──────────────────────────────────────────────────
def get_txn():
    df = st.session_state.transactions.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["Amount"] = df["Amount"].astype(float)
    return df

def income_total(df): return df[df["Type"] == "Income"]["Amount"].sum()
def expense_total(df): return df[df["Type"] == "Expense"]["Amount"].sum()

# ─── UI ───────────────────────────────────────────────────────
st.title("💰 Finance & Accounting")
st.caption("P&L · Cash Flow · GST · Accounts Payable / Receivable · Ledger")

tabs = st.tabs([
    "📊 P&L Dashboard",
    "📒 Transaction Ledger",
    "💳 Payables",
    "📥 Receivables",
    "🧾 GST Summary",
    "📈 Cash Flow",
])

df = get_txn()
total_in = income_total(df)
total_ex = expense_total(df)
net_profit = total_in - total_ex

# ══════════════════════════════════════════════════════════════
# TAB 1: P&L DASHBOARD
# ══════════════════════════════════════════════════════════════
with tabs[0]:
    st.subheader("📊 Profit & Loss Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"₹{total_in:,.0f}", delta="↑ This period")
    col2.metric("Total Expenses", f"₹{total_ex:,.0f}")
    profit_color = "normal" if net_profit >= 0 else "inverse"
    col3.metric("Net Profit", f"₹{net_profit:,.0f}",
                delta=f"{net_profit/total_in*100:.1f}% margin" if total_in else None)
    gst_collected = df[df["Type"] == "Income"]["Tax_GST"].sum()
    gst_paid = df[df["Type"] == "Expense"]["Tax_GST"].sum()
    col4.metric("GST Liability (Net)", f"₹{gst_collected - gst_paid:,.0f}")

    col_l, col_r = st.columns(2)
    with col_l:
        # Income vs Expense by category
        cat_df = df.groupby(["Type", "Category"])["Amount"].sum().reset_index()
        fig_cat = px.bar(cat_df, x="Category", y="Amount", color="Type",
                         barmode="group", title="Income vs Expense by Category",
                         color_discrete_map={"Income": "#2ECC71", "Expense": "#E74C3C"})
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_r:
        # Expense breakdown pie
        exp_df = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().reset_index()
        fig_exp = px.pie(exp_df, values="Amount", names="Category",
                         title="Expense Breakdown", hole=0.4,
                         color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_exp, use_container_width=True)

    # Monthly trend
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    monthly = df.groupby(["Month", "Type"])["Amount"].sum().reset_index()
    fig_trend = px.line(monthly, x="Month", y="Amount", color="Type",
                        title="Monthly Income vs Expense Trend",
                        color_discrete_map={"Income": "#2ECC71", "Expense": "#E74C3C"},
                        markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

# ══════════════════════════════════════════════════════════════
# TAB 2: TRANSACTION LEDGER
# ══════════════════════════════════════════════════════════════
with tabs[1]:
    st.subheader("📒 Transaction Ledger")

    # Filters
    fc1, fc2, fc3 = st.columns(3)
    type_f = fc1.multiselect("Type", ["Income", "Expense"], default=["Income", "Expense"])
    cat_f = fc2.multiselect("Category", df["Category"].unique().tolist(),
                             default=df["Category"].unique().tolist())
    date_range = fc3.date_input("Date Range",
                                 value=(date.today() - timedelta(days=90), date.today()),
                                 key="ledger_dates")

    filtered = df[
        (df["Type"].isin(type_f)) &
        (df["Category"].isin(cat_f))
    ]
    if len(date_range) == 2:
        filtered = filtered[
            (filtered["Date"] >= pd.Timestamp(date_range[0])) &
            (filtered["Date"] <= pd.Timestamp(date_range[1]))
        ]

    st.dataframe(
        filtered.sort_values("Date", ascending=False).style.apply(
            lambda r: ["color: #2ECC71" if r["Type"] == "Income" else "color: #E74C3C" for _ in r],
            axis=1
        ),
        use_container_width=True, hide_index=True
    )

    st.subheader("➕ Add Transaction")
    with st.expander("New Transaction Entry"):
        t1, t2, t3 = st.columns(3)
        with t1:
            txn_date = st.date_input("Date", value=date.today())
            txn_type = st.selectbox("Type", ["Income", "Expense"])
            txn_cat = st.selectbox("Category", [
                "Sales", "Services", "Interest", "Other Income",
                "Raw Material", "Operations", "Salaries", "Marketing",
                "Logistics", "Tax", "Utilities", "Rent", "Other Expense"
            ])
        with t2:
            txn_desc = st.text_input("Description")
            txn_amount = st.number_input("Amount (₹)", min_value=0.0, step=100.0)
            txn_gst = st.number_input("GST Amount (₹)", min_value=0.0, step=10.0)
        with t3:
            txn_mode = st.selectbox("Payment Mode", ["Cash", "UPI", "Cheque", "Bank Transfer", "Wire Transfer", "Online"])
            txn_ref = st.text_input("Reference No.")
        if st.button("💾 Save Transaction", type="primary"):
            new_txn = pd.DataFrame([{
                "Date": str(txn_date), "Type": txn_type, "Category": txn_cat,
                "Description": txn_desc, "Amount": txn_amount,
                "Tax_GST": txn_gst, "Payment_Mode": txn_mode, "Reference": txn_ref
            }])
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_txn], ignore_index=True)
            st.success("✅ Transaction saved!")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 3: PAYABLES
# ══════════════════════════════════════════════════════════════
with tabs[2]:
    st.subheader("💳 Accounts Payable (What You Owe)")
    pay_df = st.session_state.payables.copy()
    pay_df["Due_Date"] = pd.to_datetime(pay_df["Due_Date"])

    overdue = pay_df[pay_df["Status"] == "Overdue"]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Payable", f"₹{pay_df['Amount'].sum():,.0f}")
    col2.metric("Overdue", f"₹{overdue['Amount'].sum():,.0f}",
                delta=f"{len(overdue)} bills overdue" if len(overdue) else "All current",
                delta_color="inverse" if len(overdue) else "normal")
    col3.metric("Due This Week", f"₹{pay_df[pay_df['Due_Date'] <= pd.Timestamp(date.today() + timedelta(7))]['Amount'].sum():,.0f}")

    st.dataframe(
        pay_df.style.apply(
            lambda r: ["background-color: #ffe0e0" if r["Status"] == "Overdue"
                       else "background-color: #fff9c4" if r["Status"] == "Pending" else "" for _ in r],
            axis=1
        ),
        use_container_width=True, hide_index=True
    )

    with st.expander("➕ Add Payable"):
        p1, p2, p3 = st.columns(3)
        vendor = p1.text_input("Vendor")
        inv_no = p1.text_input("Invoice No.")
        amount = p2.number_input("Amount (₹)", min_value=0.0, step=100.0, key="pay_amt")
        due = p2.date_input("Due Date", key="pay_due")
        status = p3.selectbox("Status", ["Pending", "Overdue", "Paid", "Partial"])
        cat = p3.selectbox("Category", ["Raw Material", "Freight", "Services", "Utilities", "Other"])
        if st.button("💾 Add Payable", type="primary"):
            new_pay = pd.DataFrame([{
                "Vendor": vendor, "Invoice_No": inv_no, "Amount": amount,
                "Due_Date": str(due), "Status": status, "Category": cat
            }])
            st.session_state.payables = pd.concat([st.session_state.payables, new_pay], ignore_index=True)
            st.success("✅ Payable added!")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 4: RECEIVABLES
# ══════════════════════════════════════════════════════════════
with tabs[3]:
    st.subheader("📥 Accounts Receivable (What You're Owed)")
    rec_df = st.session_state.receivables.copy()
    rec_df["Due_Date"] = pd.to_datetime(rec_df["Due_Date"])
    rec_df["Outstanding"] = rec_df["Amount"] - rec_df["Paid"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Receivable", f"₹{rec_df['Amount'].sum():,.0f}")
    col2.metric("Amount Collected", f"₹{rec_df['Paid'].sum():,.0f}")
    col3.metric("Outstanding Balance", f"₹{rec_df['Outstanding'].sum():,.0f}")

    st.dataframe(rec_df, use_container_width=True, hide_index=True)

    with st.expander("➕ Add Receivable"):
        r1, r2, r3 = st.columns(3)
        cust = r1.text_input("Customer")
        inv_r = r1.text_input("Invoice No.", key="rec_inv")
        amt_r = r2.number_input("Invoice Amount (₹)", min_value=0.0, step=100.0, key="rec_amt")
        paid_r = r2.number_input("Amount Already Paid (₹)", min_value=0.0, step=100.0, key="rec_paid")
        due_r = r3.date_input("Due Date", key="rec_due")
        stat_r = r3.selectbox("Status", ["Pending", "Partial", "Paid", "Overdue"])
        if st.button("💾 Add Receivable", type="primary"):
            new_rec = pd.DataFrame([{
                "Customer": cust, "Invoice_No": inv_r, "Amount": amt_r,
                "Due_Date": str(due_r), "Status": stat_r, "Paid": paid_r
            }])
            st.session_state.receivables = pd.concat([st.session_state.receivables, new_rec], ignore_index=True)
            st.success("✅ Receivable added!")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# TAB 5: GST SUMMARY
# ══════════════════════════════════════════════════════════════
with tabs[4]:
    st.subheader("🧾 GST Summary")
    st.info("Monthly GST liability calculation — for filing GSTR-1 / GSTR-3B")

    df_gst = get_txn()
    df_gst["Month"] = df_gst["Date"].dt.to_period("M").astype(str)

    gst_monthly = df_gst.groupby(["Month", "Type"])["Tax_GST"].sum().reset_index()
    gst_pivot = gst_monthly.pivot(index="Month", columns="Type", values="Tax_GST").fillna(0)
    if "Income" in gst_pivot.columns and "Expense" in gst_pivot.columns:
        gst_pivot["Net_GST_Liability"] = gst_pivot["Income"] - gst_pivot["Expense"]
    elif "Income" in gst_pivot.columns:
        gst_pivot["Net_GST_Liability"] = gst_pivot["Income"]
    gst_pivot.columns.name = None
    gst_pivot = gst_pivot.rename(columns={
        "Income": "GST Collected (Output)",
        "Expense": "GST Paid (Input)",
    }).reset_index()

    st.dataframe(gst_pivot.style.format({
        "GST Collected (Output)": "₹{:.0f}",
        "GST Paid (Input)": "₹{:.0f}",
        "Net_GST_Liability": "₹{:.0f}",
    }), use_container_width=True, hide_index=True)

    fig_gst = px.bar(gst_pivot, x="Month",
                     y=["GST Collected (Output)", "GST Paid (Input)"],
                     barmode="group", title="GST Collected vs Paid",
                     color_discrete_sequence=["#3498DB", "#E74C3C"])
    st.plotly_chart(fig_gst, use_container_width=True)

    total_out = df_gst[df_gst["Type"] == "Income"]["Tax_GST"].sum()
    total_in_gst = df_gst[df_gst["Type"] == "Expense"]["Tax_GST"].sum()
    net = total_out - total_in_gst
    col1, col2, col3 = st.columns(3)
    col1.metric("Output GST (Collected)", f"₹{total_out:,.0f}")
    col2.metric("Input GST (Paid)", f"₹{total_in_gst:,.0f}")
    col3.metric("Net GST Payable to Govt", f"₹{net:,.0f}")

# ══════════════════════════════════════════════════════════════
# TAB 6: CASH FLOW
# ══════════════════════════════════════════════════════════════
with tabs[5]:
    st.subheader("📈 Cash Flow Statement")

    df_cf = get_txn().sort_values("Date")
    df_cf["Flow"] = df_cf.apply(lambda r: r["Amount"] if r["Type"] == "Income" else -r["Amount"], axis=1)
    df_cf["Cumulative_Balance"] = df_cf["Flow"].cumsum()

    fig_cf = go.Figure()
    fig_cf.add_trace(go.Scatter(
        x=df_cf["Date"], y=df_cf["Cumulative_Balance"],
        mode="lines+markers", name="Cash Balance",
        line=dict(color="#2ECC71", width=2),
        fill="tozeroy", fillcolor="rgba(46,204,113,0.1)"
    ))
    fig_cf.update_layout(title="Cumulative Cash Flow", xaxis_title="Date",
                         yaxis_title="Balance (₹)", height=350)
    st.plotly_chart(fig_cf, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_in = px.bar(df_cf[df_cf["Type"] == "Income"].sort_values("Date"),
                        x="Date", y="Amount", color="Category",
                        title="Cash Inflows by Category")
        st.plotly_chart(fig_in, use_container_width=True)
    with col2:
        fig_out = px.bar(df_cf[df_cf["Type"] == "Expense"].sort_values("Date"),
                         x="Date", y="Amount", color="Category",
                         title="Cash Outflows by Category",
                         color_discrete_sequence=px.colors.qualitative.Set1)
        st.plotly_chart(fig_out, use_container_width=True)

    # Summary table
    st.subheader("Summary")
    summary = {
        "Opening Balance (assumed)": 0,
        "Total Inflows": total_in,
        "Total Outflows": total_ex,
        "Net Cash Flow": net_profit,
    }
    sum_df = pd.DataFrame(list(summary.items()), columns=["Item", "Amount (₹)"])
    st.dataframe(sum_df.style.format({"Amount (₹)": "₹{:,.0f}"}),
                 use_container_width=True, hide_index=True)
