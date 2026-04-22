import streamlit as st
import pandas as pd
import sqlite3

conn = sqlite3.connect("banksight.db")

st.title("🧠 Analytical Insights")

queries = {

"Q1 Customers per city & avg balance": """
SELECT c.city, COUNT(*) total_customers, AVG(a.account_balance) avg_balance
FROM customers c JOIN accounts a
ON c.customer_id = a.customer_id
GROUP BY c.city
""",

"Q2 Highest balance account type": """
SELECT account_type, SUM(account_balance) total_balance
FROM customers c JOIN accounts a
ON c.customer_id = a.customer_id
GROUP BY account_type
ORDER BY total_balance DESC
""",

"Q3 Top 10 customers": """
SELECT c.name, SUM(a.account_balance) total_balance
FROM customers c JOIN accounts a
ON c.customer_id = a.customer_id
GROUP BY c.customer_id
ORDER BY total_balance DESC
LIMIT 10
""",

"Q4 2023 high balance customers": """
SELECT *
FROM customers c JOIN accounts a
ON c.customer_id = a.customer_id
WHERE strftime('%Y', join_date)='2023'
AND account_balance > 100000
""",

"Q5 Transaction volume": """
SELECT txn_type, SUM(amount) total
FROM transactions GROUP BY txn_type
""",

"Q6 Failed transactions": """
SELECT txn_type, COUNT(*) failed_count
FROM transactions
WHERE status='failed'
GROUP BY txn_type
""",

"Q7 Total transactions count": """
SELECT txn_type, COUNT(*) total
FROM transactions GROUP BY txn_type
""",

"Q8 High value accounts": """
SELECT customer_id, COUNT(*) cnt
FROM transactions
WHERE amount > 20000
GROUP BY customer_id
HAVING COUNT(*) >= 5
""",

"Q9 Loan avg & interest": """
SELECT Loan_Type, AVG(Loan_Amount), AVG(Interest_Rate)
FROM loans GROUP BY Loan_Type
""",

"Q10 Multiple loans customers": """
SELECT Customer_ID, COUNT(*) loans
FROM loans
WHERE Loan_Status IN ('Active','Approved')
GROUP BY Customer_ID
HAVING COUNT(*) > 1
""",

"Q11 Top loan holders": """
SELECT Customer_ID, SUM(Loan_Amount) total
FROM loans
WHERE Loan_Status != 'Closed'
GROUP BY Customer_ID
ORDER BY total DESC
LIMIT 5
""",

"Q12 Avg loan per branch": """
SELECT Branch, AVG(Loan_Amount)
FROM loans GROUP BY Branch
""",

"Q13 Age groups": """
SELECT 
CASE 
WHEN age BETWEEN 18 AND 25 THEN '18-25'
WHEN age BETWEEN 26 AND 35 THEN '26-35'
WHEN age BETWEEN 36 AND 50 THEN '36-50'
ELSE '50+' END AS age_group,
COUNT(*) total
FROM customers
GROUP BY age_group
""",

"Q14 Resolution time": """
SELECT Issue_Category,
AVG(julianday(Date_Closed)-julianday(Date_Opened)) avg_days
FROM support_tickets
GROUP BY Issue_Category
""",

"Q15 Best agents": """
SELECT Support_Agent, COUNT(*) total
FROM support_tickets
WHERE Priority='Critical' AND Customer_Rating>=4
GROUP BY Support_Agent
ORDER BY total DESC
"""
}

choice = st.selectbox("Select Query", list(queries.keys()))

query = queries[choice]

st.code(query)

df = pd.read_sql(query, conn)

st.dataframe(df, use_container_width=True)