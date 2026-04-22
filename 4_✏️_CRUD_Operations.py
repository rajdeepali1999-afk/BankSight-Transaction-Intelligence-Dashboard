import streamlit as st
import sqlite3

conn = sqlite3.connect("banksight.db")

st.title("✏️ CRUD Operations")

# CREATE
st.subheader("Add Customer")
cid = st.text_input("Customer ID")
name = st.text_input("Name")
city = st.text_input("City")

if st.button("Add Customer"):
    conn.execute(f"""
    INSERT INTO customers (customer_id, name, city)
    VALUES ('{cid}','{name}','{city}')
    """)
    conn.commit()
    st.success("Added!")

# DELETE
st.subheader("Delete Customer")
del_id = st.text_input("Enter Customer ID")

if st.button("Delete"):
    conn.execute(f"DELETE FROM customers WHERE customer_id='{del_id}'")
    conn.commit()
    st.warning("Deleted!")