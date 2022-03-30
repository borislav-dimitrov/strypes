import tkinter as tk
import customtkinter as ctk


class MyCustomTkinter:
    def __init__(self, root, resolution: tuple, rows: int = 30, cols: int = 30):
        self.ww = resolution[0]
        self.wh = resolution[1]
        self.root = root
        self.rows = rows
        self.cols = cols
        x = (root.winfo_screenwidth() / 2) - (self.ww / 2)
        y = (root.winfo_screenheight() / 2) - (self.wh / 2)
        root.geometry("%dx%d+%d+%d" % (self.ww, self.wh, x, y))

        self.set_grid()

        self.btn1 = ctk.CTkButton(self.root, text="Button 1")
        self.btn2 = ctk.CTkButton(self.root, text="Button 2")

        self.btn1.grid(row=1, column=0, sticky="nsew")
        self.btn2.grid(row=3, column=0, sticky="nsew")

    def set_grid(self):
        for row in range(0, self.rows):
            tk.Grid.rowconfigure(self.root, row, weight=1)
        for col in range(0, self.cols):
            tk.Grid.columnconfigure(self.root, col, weight=1)
