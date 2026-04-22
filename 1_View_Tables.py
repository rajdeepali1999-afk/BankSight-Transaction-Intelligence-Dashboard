import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("banksight.db")

st.title("📊 View Tables")

tables = [
    "customers", "accounts", "transactions",
    "loans", "branches", "support_tickets", "credit_cards"
]

table = st.selectbox("Select Table", tables)

df = pd.read_sql(f"SELECT * FROM {table}", conn)

st.dataframe(df, use_container_width=True)