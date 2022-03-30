import tkinter as tk
from tkinter import ttk
import time


class Loading:
    def __init__(self, root, resolution: tuple, rows: int = 30, cols: int = 30):
        root.title("Loading....")
        self.ww = resolution[0]
        self.wh = resolution[1]
        self.root = root
        self.rows = rows
        self.cols = cols
        x = (root.winfo_screenwidth() / 2) - (self.ww / 2)
        y = (root.winfo_screenheight() / 2) - (self.wh / 2)
        root.geometry("%dx%d+%d+%d" % (self.ww, self.wh, x, y))
        # root.overrideredirect(1)

        self.set_grid()

        self.bar(2)

    def set_grid(self):
        for row in range(0, self.rows):
            tk.Grid.rowconfigure(self.root, row, weight=1)
        for col in range(0, self.cols):
            tk.Grid.columnconfigure(self.root, col, weight=1)

    def bar(self, time_s: int = None):
        color1 = "#249794"
        color2 = "white"
        color3 = "gray"  # unloaded area color
        font_text = ("Calibri (Body)", 40, "bold")

        style = ttk.Style()
        style.theme_use("clam")
        # style.configure("my.Horizontal.TProgressbar", foreground=color1, background=color1,
        #                 bordercolor=color2, troughcolor=color3)
        style.layout("LabeledProgressbar",
                     [('LabeledProgressbar.trough',
                       {'children': [('LabeledProgressbar.pbar', {'side': 'left', 'sticky': 'ns'}),
                                     ("LabeledProgressbar.label",  # label inside the bar
                                      {"sticky": ""})], 'sticky': 'nswe'})])

        lbl_info = tk.Label(self.root, text="Loading please wait!", fg="orange", bg=color1, font=font_text)
        lbl_info.grid(row=0, rowspan=self.rows - 1, column=0, columnspan=self.cols, sticky="nsew")
        bar = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", style="LabeledProgressbar")
        bar.grid(row=self.rows - 1, column=0, columnspan=self.cols, sticky="nsew")

        if time_s:
            step = time_s / 200
        else:
            step = 0.01
        r = 0
        while r <= 100:
            bar["value"] = r
            style.configure("LabeledProgressbar", text=f"{r}%")
            self.root.update()
            time.sleep(step)
            r += 1

        self.root.destroy()
