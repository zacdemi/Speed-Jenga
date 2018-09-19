import os

def clear_screen():
     """ clear the terminal screen """
     os.system('cls' if os.name == 'nt' else 'clear')
