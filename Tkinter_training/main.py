import tkinter as tk
from tkinter import ttk
from tk_window import MyWindow


def main():
    window = tk.Tk()
    screen = MyWindow(window, "Login", "Login", 800, 400, 30, 30)
    window.mainloop()


if __name__ == '__main__':
    main()
