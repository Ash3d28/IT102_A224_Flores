import streamlit as st
from flores_atm_account import Account
import flores_atm_balance
import flores_atm_deposit
import flores_atm_history
import flores_atm_analysis
import flores_atm_withdraw

account = Account("Juan Dela Cruz", 10000.00)
st.set_page_config(
    page_title="Python ATM",
    page_icon="🏦",
    layout="wide"
)
st.title("PYTHON ATM")
st.write(
    f"Welcome, **{account.account_name}**!"
)

st.divider()
st.sidebar.title("ATM MENU")

choice = st.sidebar.radio(
    "Select an option:",
    [
        "Check Balance",
        "Deposit",
        "Withdraw",
        "View History",
        "Analyze Transactions"
    ]
)

if choice == "Check Balance":
    st.header("Check Balance")
    balance = (flores_atm_balance.check_balance(account))
    st.metric("Current Balance", f"₱{balance:,.2f}")

elif choice == "Deposit":
    st.header("Deposit Money")
    amount = st.number_input(
        "Enter deposit amount",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )
    if st.button("Deposit Money"):
        if amount <= 0:
            st.error("Invalid deposit amount.")
        else:
            success = (flores_atm_deposit.deposit_money(account, amount))
            if success:
                st.success("Deposit successful.")
                st.metric("New Balance", f"₱{account.check_balance():,.2f}")

elif choice == "Withdraw":
    st.header("Withdraw Money")
    st.write(
        f"Available Balance: "
        f"₱{account.check_balance():,.2f}"
    )
    amount = st.number_input(
        "Enter withdrawal amount",
        min_value=0.0,
        step=100.0,
        format="%.2f"
    )
    if st.button("Withdraw Money"):
        if amount <= 0:
            st.error(
                "Invalid withdrawal amount."
            )
        elif amount > account.check_balance():
            st.error("Insufficient balance.")
        else:
            success = (
                flores_atm_withdraw.withdraw_money(account, amount)
            )
            if success:
                st.success("Withdrawal successful.")
                st.metric("New Balance", f"₱{account.check_balance():,.2f}")

elif choice == "View History":
    st.header("Transaction History")
    lines = (flores_atm_history.view_history())
    transactions = []
    current_transaction = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("Timestamp:"):
            current_transaction["Timestamp"] = (
                line.replace(
                    "Timestamp:", "").strip()
            )
        elif line.startswith("Account:"):
            current_transaction["Account"] = (
                line.replace("Account:", "").strip()
            )
        elif line.startswith("Transaction:"):
            current_transaction["Transaction"] = (
                line.replace("Transaction:", "").strip()
            )
        elif line.startswith("Amount:"):
            current_transaction["Amount"] = (
                line.replace("Amount: ₱", "").strip()
            )
            transactions.append(current_transaction)
            current_transaction = {}
    if transactions:
        st.dataframe(
            transactions,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No transactions available.")

elif choice == "Analyze Transactions":
    st.header("Transaction Analysis")
    result = (flores_atm_analysis.analyze_transactions())

    st.subheader("1. Transaction Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Total Transactions",
        result["total_transactions"]
    )
    col2.metric(
        "Deposits",
        result["deposits"]
    )
    col3.metric(
        "Withdrawals",
        result["withdrawals"]
    )
    st.divider()

    st.subheader("2. Transaction Amount Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Total Deposited",
        f"₱{result['total_deposited']:,.2f}"
    )
    col2.metric(
        "Total Withdrawn",
        f"₱{result['total_withdrawn']:,.2f}"
    )
    col3.metric(
        "Average Transaction",
        f"₱{result['average_transaction']:,.2f}"
    )
    st.divider()

    st.subheader("3. Account Activity Analysis")
    col1, col2, col3 = st.columns(3)
    col1.metric(
        "Latest Transaction",
        result["latest_transaction"]
    )
    col2.metric(
        "Largest Transaction",
        f"₱{result['largest_transaction']:,.2f}"
    )
    col3.metric(
        "Latest Activity",
        result["latest_timestamp"]
    )