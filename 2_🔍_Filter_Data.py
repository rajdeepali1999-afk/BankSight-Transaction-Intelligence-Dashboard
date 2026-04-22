import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("banksight.db")

st.title("🔍 Filter Data")

table = st.selectbox("Choose Dataset", ["customers", "transactions", "accounts"])

df = pd.read_sql(f"SELECT * FROM {table}", conn)

# Dynamic filters
columns = st.multiselect("Select Columns to Filter", df.columns)

filtered_df = df.copy()

for col in columns:
    unique_vals = df[col].dropna().unique()
    selected = st.multiselect(f"Filter {col}", unique_vals)
    
    if selected:
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

st.dataframe(filtered_df, use_container_width=True)