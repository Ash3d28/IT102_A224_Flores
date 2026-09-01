from datetime import datetime

def withdraw_money(account, amount):
    if amount < 0:
        return False
    else:
        check = account.withdraw(amount)
        if check == True:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
                )
            file = open("transactions.txt", "a")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Account: {account.account_name}\n")
            file.write("Transaction: Withdraw\n")
            file.write(f"Amount: ₱{amount:.2f}\n")
            file.close()
            return True
        else:
            return False
