import streamlit as st
import pandas as pd
from datetime import date

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------------------------------------------
# SESSION STATE FOR STORING TRANSACTIONS
# ---------------------------------------------------

if "transactions" not in st.session_state:
    st.session_state.transactions = []

# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------

st.sidebar.title("💰 Expense Tracker")

menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Add Transaction", "View Transactions", "Summary"]
)

# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if menu == "Home":

    st.title("💰 Personal Expense Tracker")

    st.subheader("Track Your Income and Expenses Easily")

    st.write("""
    This application helps users manage their finances by:

    ✅ Adding income details  
    ✅ Adding expense details  
    ✅ Viewing transaction history  
    ✅ Calculating total income  
    ✅ Calculating total expenses  
    ✅ Displaying remaining balance  
    ✅ Showing category-wise expense summary
    """)

    st.info("Use the sidebar to navigate through the application.")

# ---------------------------------------------------
# ADD TRANSACTION PAGE
# ---------------------------------------------------

elif menu == "Add Transaction":

    st.title("➕ Add Transaction")

    # Transaction Type
    transaction_type = st.selectbox(
        "Select Transaction Type",
        ["Income", "Expense"]
    )

    # Category/Input
    if transaction_type == "Income":

        category = st.text_input(
            "Income Source",
            placeholder="Example: Salary"
        )

    else:

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Medical",
                "Others"
            ]
        )

    # Amount
    amount = st.number_input(
        "Amount (₹)",
        min_value=0.0,
        format="%.2f"
    )

    # Date
    transaction_date = st.date_input(
        "Select Date",
        value=date.today()
    )

    # Description
    description = st.text_area(
        "Description",
        placeholder="Enter transaction details..."
    )

    # Add Button
    if st.button("Add Transaction"):

        if category == "":
            st.error("Please enter category/source.")

        elif amount <= 0:
            st.error("Amount must be greater than 0.")

        else:

            transaction = {
                "Type": transaction_type,
                "Category": category,
                "Amount": amount,
                "Date": str(transaction_date),
                "Description": description
            }

            st.session_state.transactions.append(transaction)

            st.success("✅ Transaction Added Successfully!")

# ---------------------------------------------------
# VIEW TRANSACTIONS PAGE
# ---------------------------------------------------

elif menu == "View Transactions":

    st.title("📋 Transaction History")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning("No transactions available.")

# ---------------------------------------------------
# SUMMARY PAGE
# ---------------------------------------------------

elif menu == "Summary":

    st.title("📊 Financial Summary")

    if st.session_state.transactions:

        df = pd.DataFrame(st.session_state.transactions)

        # Total Income
        total_income = df[df["Type"] == "Income"]["Amount"].sum()

        # Total Expense
        total_expense = df[df["Type"] == "Expense"]["Amount"].sum()

        # Balance
        balance = total_income - total_expense

        # Display Metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💵 Total Income",
                f"₹ {total_income:.2f}"
            )

        with col2:
            st.metric(
                "💸 Total Expenses",
                f"₹ {total_expense:.2f}"
            )

        with col3:
            st.metric(
                "💰 Balance",
                f"₹ {balance:.2f}"
            )

        st.divider()

        # Category-wise Expense Summary
        st.subheader("📌 Category-wise Expense Summary")

        expense_df = df[df["Type"] == "Expense"]

        if not expense_df.empty:

            category_summary = expense_df.groupby(
                "Category"
            )["Amount"].sum().reset_index()

            category_summary.columns = [
                "Category",
                "Total Spent (₹)"
            ]

            st.dataframe(
                category_summary,
                use_container_width=True
            )

            # Bar Chart
            st.bar_chart(
                category_summary.set_index("Category")
            )

        else:
            st.info("No expense transactions available.")

    else:
        st.warning("No transactions available.")