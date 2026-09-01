from datetime import datetime
#import flores_atm_balance

def deposit_money(account, amount):
    if amount < 0 :
        return False
    else:
        check = account.deposit(amount)
        if check == True:
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
                )
            file = open("transactions.txt", "a")
            file.write(f"Timestamp: {timestamp}\n")
            file.write(f"Account: {account.account_name}\n")
            file.write("Transaction: Deposit\n")
            file.write(f"Amount: ₱{amount:.2f}\n")
            file.close()
            #print("Deposit successful.")
            return True
        else:
            return False

""" 
######### Learning Signature ######### 
Programmed by: Flores Daryl
Date Submitted: September 01, 2026
 
Program Description: This program is about GUI's with the ATM system!
Reflection: I learned about timestamps, woah.

AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
