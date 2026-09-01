from datetime import datetime

def withdraw_money(account, amount):
    if amount < 0:
        return False
    else:
        check = account.withdraw()
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

""" 
######### Learning Signature ######### 
Programmed by: Flores Daryl
Date Submitted: September 01, 2026
 
Program Description: This program is an activity where we touch on OOP!
Reflection: I learned about timestamps, woah.

AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
