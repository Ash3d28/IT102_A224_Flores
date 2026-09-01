class Account:
    def __init__(self, name, starting_balance):
        self.account_name = name
        self._balance = starting_balance

    def check_balance(self):
        return self._balance
        #print(f"Current Balance: ₱{self._balance:.2f}")

    def deposit(self, amount):
        if amount > 0:
            self._balance = self._balance + amount
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self._balance:
            self._balance = self._balance - amount
            return True
        else:
            return False

""" 
######### Learning Signature ######### 
Programmed by: Flores Daryl
Date Submitted: September 01, 2026
 
Program Description: This program is about GUI's with the ATM system!
Reflection: I learned that I will be using streamlit to create the interface

AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
