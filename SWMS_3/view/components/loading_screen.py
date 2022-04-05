import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import time
import resources.theme_cfg as tcfg


class Loading:
    def __init__(self, root, resolution: tuple = (640, 360), rows: int = 30, cols: int = 30, time_s=1):
        root.title("Loading....")
        self.ww = resolution[0]
        self.wh = resolution[1]
        self.root = root
        self.rows = rows
        self.cols = cols
        self.MAIN_COLOR = tcfg._MAIN_COLOR
        self.HOVER_COLOR = tcfg._HOVER_COLOR
        self.TEXT_COLOR = tcfg._TEXT_COLOR
        x = (root.winfo_screenwidth() / 2) - (self.ww / 2)
        y = (root.winfo_screenheight() / 2) - (self.wh / 2)
        root.geometry("%dx%d+%d+%d" % (self.ww, self.wh, x, y))
        # root.overrideredirect(1)

        self.set_grid()

        self.bar(time_s)

    def set_grid(self):
        for row in range(0, self.rows):
            tk.Grid.rowconfigure(self.root, row, weight=1)
        for col in range(0, self.cols):
            tk.Grid.columnconfigure(self.root, col, weight=1)

    def bar(self, time_s: int):
        font_text = ("Calibri (Body)", 40, "bold")

        style = ttk.Style()
        style.theme_use("clam")

        lbl_info = ctk.CTkLabel(self.root, text="Loading...\nPlease wait!", text_color=self.MAIN_COLOR,
                                text_font=font_text)
        lbl_info.grid(row=0, rowspan=self.rows - 1, column=0, columnspan=self.cols, sticky="nsew")
        bar = ctk.CTkProgressBar(self.root)
        bar.grid(row=self.rows - 2, rowspan=2, column=0, columnspan=self.cols, sticky="nsew")

        step = time_s / 200
        r = 0
        while r <= 1:
            # bar["variable"] = r
            bar.set(r)
            self.root.update()
            time.sleep(step)
            r += 0.01
        self.root.destroy()
