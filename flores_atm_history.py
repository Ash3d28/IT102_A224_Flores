def view_history():
    try:
        file = open("transactions.txt", "r")
        lines = file.readlines()
        file.close()
        return lines
    except FileNotFoundError:
        return []


