import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(layout="wide")

conn = sqlite3.connect("banksight.db")

st.title("📈 BankSight Executive Dashboard")

# ==============================
# 📌 LOAD DATA
# ==============================
customers = pd.read_sql("SELECT * FROM customers", conn)
transactions = pd.read_sql("SELECT * FROM transactions", conn)
accounts = pd.read_sql("SELECT * FROM accounts", conn)
loans = pd.read_sql("SELECT * FROM loans", conn)

# ==============================
# 📌 KPI METRICS
# ==============================
total_customers = customers.shape[0]
total_transactions = transactions.shape[0]
total_balance = accounts['account_balance'].sum()
total_loans = loans['Loan_Amount'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Customers", total_customers)
col2.metric("💳 Transactions", total_transactions)
col3.metric("💰 Total Balance", f"₹{int(total_balance):,}")
col4.metric("🏦 Loans Issued", f"₹{int(total_loans):,}")

st.divider()

# ==============================
# 📊 CHART 1: TRANSACTION TYPE
# ==============================
txn_chart = transactions.groupby("txn_type")["amount"].sum().reset_index()

fig1 = px.bar(
    txn_chart,
    x="txn_type",
    y="amount",
    title="Transaction Volume by Type",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# ==============================
# 📊 CHART 2: CITY DISTRIBUTION
# ==============================
city_chart = customers['city'].value_counts().reset_index()
city_chart.columns = ['city', 'count']

fig2 = px.pie(
    city_chart,
    names="city",
    values="count",
    title="Customer Distribution by City"
)

st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 📊 CHART 3: LOAN TYPES
# ==============================
loan_chart = loans.groupby("Loan_Type")["Loan_Amount"].sum().reset_index()

fig3 = px.bar(
    loan_chart,
    x="Loan_Type",
    y="Loan_Amount",
    title="Loan Distribution by Type",
    color="Loan_Type"
)

st.plotly_chart(fig3, use_container_width=True)

# ==============================
# 📊 CHART 4: TRANSACTION TREND
# ==============================
transactions['txn_time'] = pd.to_datetime(transactions['txn_time'])

trend = transactions.groupby(transactions['txn_time'].dt.date)["amount"].sum().reset_index()

fig4 = px.line(
    trend,
    x="txn_time",
    y="amount",
    title="Daily Transaction Trend"
)

st.plotly_chart(fig4, use_container_width=True)

# ==============================
# 🚨 FRAUD DETECTION
# ==============================
st.subheader("🚨 Fraud Detection Insights")

transactions['z_score'] = (
    (transactions['amount'] - transactions['amount'].mean()) /
    transactions['amount'].std()
)

fraud = transactions[transactions['z_score'].abs() > 3]

st.metric("⚠️ Suspicious Transactions", fraud.shape[0])

st.dataframe(fraud.head(10), use_container_width=True)

# ==============================
# 🏆 TOP CUSTOMERS
# ==============================
st.subheader("🏆 Top 5 Customers")

top_customers = pd.read_sql("""
SELECT c.name, SUM(a.account_balance) AS balance
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id
ORDER BY balance DESC
LIMIT 5
""", conn)

st.dataframe(top_customers, use_container_width=True)