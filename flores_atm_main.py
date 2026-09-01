from flores_atm_account import Account
import flores_atm_balance
import flores_atm_deposit
import flores_atm_history
import flores_atm_analysis

account = Account("Juan Dela Cruz", 10000.00)
print("==============================")
print("  PYTHON CLI ATM by FLORES")
print(f"  Welcome, {account.account_name}!")
print("==============================")
print()
print("===== ATM MENU by FLORES =====")
print("1. Check Balance")
print("2. Deposit")
print("3. View History")
print("4. Analyze Transactions")
print("5. Exit")

#unlike activity 7, i put while loop this time
# i just want  the convenience....
while True:
    choice = input("Choose option: ")
    if choice == "1":
        flores_atm_balance.check_balance(account)
    elif choice == "2":
        flores_atm_deposit.deposit_money(account)
    elif choice == "3":
        flores_atm_history.view_history()
    elif choice == "4":
        flores_atm_analysis.analyze_transactions()
    elif choice == "5":
        print("Ty ty for using my atm <3")
        break
    else:
        print("Invalid option.")

    
""" 
######### Learning Signature ######### 
Programmed by: Flores Daryl
Date Submitted: September 01, 2026
 
Program Description: This program is an activity where we touch on OOP!
Reflection: I learned how to import a class and call a method from it

AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
