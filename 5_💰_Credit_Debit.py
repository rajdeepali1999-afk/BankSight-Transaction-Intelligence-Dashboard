import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("banksight.db")

st.title("💰 Credit / Debit Simulation")

cid = st.text_input("Customer ID")

if cid:
    balance = pd.read_sql(f"""
    SELECT account_balance FROM accounts
    WHERE customer_id='{cid}'
    """, conn)

    if not balance.empty:
        st.write("Current Balance:", balance.iloc[0][0])

        amount = st.number_input("Amount")

        if st.button("Deposit"):
            conn.execute(f"""
            UPDATE accounts
            SET account_balance = account_balance + {amount}
            WHERE customer_id='{cid}'
            """)
            conn.commit()
            st.success("Deposited!")

        if st.button("Withdraw"):
            if balance.iloc[0][0] - amount >= 1000:
                conn.execute(f"""
                UPDATE accounts
                SET account_balance = account_balance - {amount}
                WHERE customer_id='{cid}'
                """)
                conn.commit()
                st.success("Withdrawn!")
            else:
                st.error("Minimum balance ₹1000 required")