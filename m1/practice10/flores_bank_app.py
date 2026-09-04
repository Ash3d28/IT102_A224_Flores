from datetime import datetime

import streamlit as st

import flores_bank_auth
import flores_bank_storage
import flores_bank_transactions
import flores_bank_analysis
import flores_bank_utils


DAILY_WITHDRAWAL_LIMIT = 10000

# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Flores Bank",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "account" not in st.session_state:

    st.session_state.account = None


# ==========================================
# BANK HEADER
# ==========================================

st.title("Flores BANK")

st.caption(
    "Secure Digital Banking System"
)

# ==========================================
# LOGIN / REGISTRATION
# ==========================================

if not st.session_state.logged_in:

    login_tab, register_tab = st.tabs(
        [
            "Login",
            "Register"
        ]
    )

    # ======================================
    # LOGIN
    # ======================================

    with login_tab:

        st.subheader(
            "Welcome Back"
        )

        account_number = st.text_input(
            "Account Number",
            key="login_account"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            key="login_pin"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            account, message = (
                flores_bank_auth
                .login_account(
                    account_number,
                    pin
                )
            )

            if account is not None:

                st.session_state.logged_in = True

                st.session_state.account = (
                    account
                )

                st.success(message)

                st.rerun()

            else:

                st.error(message)

    # ======================================
    # REGISTRATION
    # ======================================

    with register_tab:

        st.subheader(
            "Create Your Bank Account"
        )

        name = st.text_input(
            "Full Name",
            key="register_name"
        )

        account_number = st.text_input(
            "Account Number",
            key="register_account"
        )

        pin = st.text_input(
            "Create 4-Digit PIN",
            type="password",
            key="register_pin"
        )

        confirm_pin = st.text_input(
            "Confirm PIN",
            type="password",
            key="register_confirm_pin"
        )

        account_type = st.selectbox(
            "Account Type",
            [
                "Savings Account",
                "Student Account"
            ]
        )

        starting_balance = st.number_input(
            "Starting Balance",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            account, message = (
                flores_bank_auth
                .register_account(
                    name,
                    account_number,
                    pin,
                    confirm_pin,
                    account_type,
                    starting_balance
                )
            )

            if account is not None:

                st.success(message)

                st.info(
                    "Your account has been created. "
                    "Please use the Login tab."
                )

            else:

                st.error(message)

# ==========================================
# LOGGED-IN BANKING APPLICATION
# ==========================================

else:

    account = (
        st.session_state.account
    )

    # ======================================
    # SIDEBAR
    # ======================================

    st.sidebar.title(
        "Flores Bank"
    )

    st.sidebar.write(
        f"**{account.account_name}**"
    )

    st.sidebar.caption(
        account.get_account_type()
    )

    st.sidebar.write(
        f"Account: "
        f"{account.account_number}"
    )

    with st.bottom:
        menu = st.segmented_control(
            "BANKING MENU",
            [
                "📊 Dashboard",
                "💰 Deposit",
                "💸 Withdraw",
                "📝 Transaction History",
                "📈 Transaction Analysis",
                "🎁 Rewards Hub"
            ],
            default="📊 Dashboard"
        )

    with st.sidebar.expander(
        "Change PIN"
    ):

        current_pin = st.text_input(
            "Current PIN",
            type="password",
            key="current_pin"
        )

        new_pin = st.text_input(
            "New 4-Digit PIN",
            type="password",
            key="new_pin"
        )

        confirm_new_pin = st.text_input(
            "Confirm New PIN",
            type="password",
            key="confirm_new_pin"
        )

        if st.button(
            "Update PIN",
            use_container_width=True
        ):

            if not account.verify_pin(
                current_pin
            ):

                st.error(
                    "Current PIN is incorrect."
                )

            elif not flores_bank_auth.validate_pin(
                new_pin
            ):

                st.error(
                    "PIN must contain exactly 4 digits."
                )

            elif new_pin != confirm_new_pin:

                st.error(
                    "PIN confirmation does not match."
                )

            else:

                account.set_pin(
                    new_pin
                )

                flores_bank_storage.update_account(
                    account
                )

                st.success(
                    "PIN updated successfully."
                )

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):
        st.session_state.logged_in = False

        st.session_state.account = None

        st.rerun()


    # ======================================
    # DASHBOARD
    # ======================================

    if menu == "📊 Dashboard":

        with st.container(border=True):
            st.header(
                f"Welcome, {account.account_name}"
            )

            st.subheader(
                "Account Overview"
            )

            st.divider()

            col1, = st.columns(1)

            col1.metric(
                "Current Balance",
                flores_bank_utils
                .format_currency(
                    account.check_balance()
                )
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "Account Type",
                account.get_account_type()
            )


            col2.metric(
                "Account Number",
                account.account_number
            )

    # ======================================
    # DEPOSIT
    # ======================================

    elif menu == "💰 Deposit":

        st.header(
            "Deposit Money"
        )

        st.write(
            f"Current Balance: "
            f"**{flores_bank_utils.format_currency(account.check_balance())}**"
        )

        amount = st.number_input(
            "Deposit Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "Confirm Deposit",
            use_container_width=True
        ):

            if not flores_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid deposit amount."
                )

            else:

                success = account.deposit(
                    amount
                )

                if success:

                    flores_bank_storage.update_account(
                        account
                    )

                    flores_bank_transactions.record_transaction(
                        account,
                        "Deposit",
                        amount
                    )

                    st.success(
                        "Deposit successful."
                    )

                    st.metric(
                        "New Balance",
                        flores_bank_utils
                        .format_currency(
                            account.check_balance()
                        )
                    )


    # ======================================
    # WITHDRAW
    # ======================================

    elif menu == "💸 Withdraw":

        st.header(
            "Withdraw Money"
        )

        st.write(
            f"Available Balance: "
            f"**{flores_bank_utils.format_currency(account.check_balance())}**"
        )

        today = datetime.now().date()
        withdrawn_today = 0

        for transaction in (
            flores_bank_transactions
            .get_transactions()
        ):

            if (
                transaction.get(
                    "account_number"
                ) == account.account_number
                and
                transaction.get(
                    "transaction"
                ) == "Withdraw"
            ):

                transaction_date = datetime.strptime(
                    transaction.get(
                        "timestamp"
                    ),
                    "%Y-%m-%d %H:%M:%S"
                ).date()

                if transaction_date == today:

                    withdrawn_today += transaction.get(
                        "amount",
                        0
                    )

        st.write(
            f"Daily Withdrawal Limit: "
            f"**{flores_bank_utils.format_currency(DAILY_WITHDRAWAL_LIMIT)}**"
        )

        st.write(
            f"Withdrawn Today: "
            f"**{flores_bank_utils.format_currency(withdrawn_today)}**"
        )

        amount = st.number_input(
            "Withdrawal Amount",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )


        if st.button(
            "Confirm Withdrawal",
            use_container_width=True
        ):

            if not flores_bank_utils.is_valid_amount(
                amount
            ):

                st.error(
                    "Invalid withdrawal amount."
                )

            elif (
                withdrawn_today + amount
                > DAILY_WITHDRAWAL_LIMIT
            ):

                st.error(
                    "Daily withdrawal limit exceeded."
                )

            elif amount > account.check_balance():

                st.error(
                    "Insufficient balance."
                )

            else:

                success = account.withdraw(
                    amount
                )

                if success:

                    flores_bank_storage.update_account(
                        account
                    )

                    flores_bank_transactions.record_transaction(
                        account,
                        "Withdraw",
                        amount
                    )

                    st.success(
                        "Withdrawal successful."
                    )

                    st.metric(
                        "New Balance",
                        flores_bank_utils
                        .format_currency(
                            account.check_balance()
                        )
                    )


    # ======================================
    # TRANSACTION HISTORY
    # ======================================

    elif menu == "📝 Transaction History":

        st.header(
            "Transaction History"
        )

        transactions = (
            flores_bank_transactions
            .get_transactions()
        )


        # Show only transactions
        # belonging to the logged-in user.

        transactions = [
            transaction
            for transaction in transactions
            if transaction.get(
                "account_number"
            ) == account.account_number
        ]


        if transactions:

            display_data = []

            for transaction in transactions:

                display_data.append({

                    "Timestamp":
                        transaction.get(
                            "timestamp",
                            "N/A"
                        ),

                    "Transaction":
                        transaction.get(
                            "transaction",
                            "N/A"
                        ),

                    "Amount":
                        flores_bank_utils
                        .format_currency(
                            transaction.get(
                                "amount",
                                0
                            )
                        ),

                    "Balance After":
                        flores_bank_utils
                        .format_currency(
                            transaction.get(
                                "balance_after",
                                0
                            )
                        )
                })


            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No transaction history available."
            )


    # ======================================
    # TRANSACTION ANALYSIS
    # ======================================

    elif menu == "📈 Transaction Analysis":

        with st.container(border=True):

            st.header(
                "Transaction Analysis"
            )

            result = (
                flores_bank_analysis
                .analyze_transactions(
                    account.account_number
                )
            )


            # ==================================
            # ANALYSIS 1
            # TRANSACTION SUMMARY
            # ==================================

            st.subheader(
                "1. Transaction Summary"
            )

            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Total Transactions",
                result[
                    "total_transactions"
                ]
            )


            col2.metric(
                "Deposits",
                result[
                    "deposits"
                ]
            )


            col3.metric(
                "Withdrawals",
                result[
                    "withdrawals"
                ]
            )


            st.divider()


            # ==================================
            # ANALYSIS 2
            # MONEY FLOW
            # ==================================

            st.subheader(
                "2. Money Flow Analysis"
            )

            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Total Deposited",
                flores_bank_utils
                .format_currency(
                    result[
                        "total_deposited"
                    ]
                )
            )


            col2.metric(
                "Total Withdrawn",
                flores_bank_utils
                .format_currency(
                    result[
                        "total_withdrawn"
                    ]
                )
            )


            col3.metric(
                "Net Cash Flow",
                flores_bank_utils
                .format_currency(
                    result[
                        "net_cash_flow"
                    ]
                )
            )


            st.divider()


            # ==================================
            # ANALYSIS 3
            # ACCOUNT ACTIVITY
            # ==================================

            st.subheader(
                "3. Account Activity Analysis"
            )

            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Largest Transaction",
                flores_bank_utils
                .format_currency(
                    result[
                        "largest_transaction"
                    ]
                )
            )


            col2.metric(
                "Average Transaction",
                flores_bank_utils
                .format_currency(
                    result[
                        "average_transaction"
                    ]
                )
            )


            col3.metric(
                "Latest Transaction",
                result[
                    "latest_transaction"
                ]
            )


            st.caption(
                f"Latest Activity: "
                f"{result['latest_timestamp']}"
            )

    elif menu == "🎁 Rewards Hub":
        st.header(
            "🎁 Rewards Hub"
        )

        points = account.get_reward_points()

        st.metric(
            "Total Reward Points",
            f"{points} PTS"
        )

        st.subheader(
            "Convert Points to Deposit Money"
        )

        points_to_redeem = st.number_input(
            "Points to Convert",
            min_value=0,
            max_value=points,
            step=10
        )

        st.caption(
            "Conversion rate: 10 Points = ₱1.00"
        )

        if st.button(
            "Convert to Deposit",
            disabled=(points_to_redeem <= 0),
            use_container_width=True
        ):

            cash_credit = points_to_redeem / 10

            if account.redeem_points_to_balance(
                points_to_redeem,
                cash_credit
            ):

                flores_bank_storage.update_account(
                    account
                )

                flores_bank_transactions.record_transaction(
                    account,
                    "Deposit",
                    cash_credit
                )

                flores_bank_transactions.record_transaction(
                    account,
                    "Rewards Redemption",
                    points_to_redeem
                )

                st.success(
                    f"Deposited {flores_bank_utils.format_currency(cash_credit)}."
                )

        st.subheader(
            "Available Rewards"
        )

        rewards = [
            "⛽ Shell Gas Voucher",
            "🍔 Jollibee Dine-In Pass",
            "🛒 Grocery Discount Voucher",
            "🎬 Movie Ticket Voucher"
        ]

        for reward in rewards:

            st.write(
                f"{reward}"
            )