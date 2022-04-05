import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import view.utils.tkinter_utils as tkutil
import resources.theme_cfg as tcfg


class InfoMessage:
    def __init__(self, message: str, buttons):
        self.root = ctk.CTk()
        self.rows = 6
        self.cols = 6
        self.FONT = ("Arial", 24, "bold")
        self.MAIN_COLOR = tcfg._MAIN_COLOR
        self.HOVER_COLOR = tcfg._HOVER_COLOR
        self.TEXT_COLOR = tcfg._TEXT_COLOR
        self.buttons = buttons

        # Set Geometry
        self.w = 400
        self.h = 200
        tkutil.center_window(self.root, self.w, self.h)
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)

        # Set Title
        self.root.title("Info")

        # Set Icon
        self.root.iconbitmap("resources/icons/i.ico")

        # Set Grid
        tkutil.setup_grid(self.root, self.rows, self.cols)
        self.disable_btns()

        self.info = ctk.CTkLabel(self.root, text=message, text_color=self.MAIN_COLOR, text_font=self.FONT)
        self.info.grid(row=0, column=0, rowspan=self.rows, columnspan=self.cols, sticky="nsew")
        self.root.mainloop()

        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def disable_btns(self):
        for btn in self.buttons:
            btn.configure(state="disabled")
        self.root.update()

    def enable_btns(self):
        for btn in self.buttons:
            btn.configure(state="normal")
        self.root.update()

    def on_exit(self):
        self.enable_btns()
        self.root.destroy()
