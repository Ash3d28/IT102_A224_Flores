def view_history():
    try:
        file = open("transactions.txt", "r")
        lines = file.readlines()
        file.close()
        return lines
    except FileNotFoundError:
        return []

""" 
######### Learning Signature ######### 
Programmed by: Flores Daryl
Date Submitted: September 01, 2026
 
Program Description: This program is about GUI's with the ATM system!
Reflection: I learned about handling an error in file searching, neat

AI Usage
[/] No AI Assistance – Completed independently without AI.
[ ] AI as Support Tool – Used AI for explanations, syntax, or minor corrections.
[ ] AI as Collaborative Partner – Used AI to design, structure, or co-create significant code.
"""
