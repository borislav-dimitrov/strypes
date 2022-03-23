import tkinter as tk
from tkinter import ttk
from login import MyLogin
from home import MyHome


def main():
    window = tk.Tk()
    # login = MyLogin(window, "Login", "Login", 800, 400, 30, 30)
    home = MyHome(window, "Home", "Simple Warehouse Management System (SWMS)", 1366, 900, 30, 30)
    window.mainloop()


if __name__ == '__main__':
    main()
