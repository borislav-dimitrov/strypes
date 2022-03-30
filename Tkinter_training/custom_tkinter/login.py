import tkinter as tk
import customtkinter as ctk


class MyCtkLogin:
    def __init__(self, m_screen, page_name, resolution: tuple, grid_rows=30, grid_cols=30):
        self.m_screen = m_screen
        self.page_name = page_name
        self.rows = grid_rows
        self.cols = grid_cols
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.colors = {"BLUE": "#1C94CF", "RED": "#871313", "LRED": "#823030", "DRED": "#731616"}

        # Set Geometry
        self.ww = resolution[0]
        self.wh = resolution[1]
        x = (self.m_screen.winfo_screenwidth() / 2) - (self.ww / 2)
        y = (self.m_screen.winfo_screenheight() / 2) - (self.wh / 2)
        self.m_screen.geometry("%dx%d+%d+%d" % (self.ww, self.wh, x, y))

        # Set Title
        self.m_screen.title(self.page_name)

        # Set Icon
        self.m_screen.iconbitmap("login_ico.ico")

        # Setup Grid
        self.setup_grid()

        # Create GUI
        # Create Header
        self.header = ctk.CTkLabel(self.m_screen, text=self.page_name, text_font=self.heading,
                                   text_color=self.colors["BLUE"])
        self.header.grid(row=0, column=1, columnspan=self.cols - 2, sticky="we")

        # Create Labels
        self.uname_lbl = ctk.CTkLabel(self.m_screen, text="Username:", text_font=self.text_bold,
                                      text_color=self.colors["BLUE"])
        self.uname_lbl.grid(row=2, column=1, columnspan=2, sticky="we")
        self.pwd_lbl = ctk.CTkLabel(self.m_screen, text="Password:", text_font=self.text_bold,
                                    text_color=self.colors["BLUE"])
        self.pwd_lbl.grid(row=3, column=1, columnspan=2, sticky="we")

        # Create Entry Fields
        self.entry1 = ctk.CTkEntry(self.m_screen, text_font=self.text_bold)
        self.entry1.grid(row=2, column=3, columnspan=5, sticky="we")
        self.entry2 = ctk.CTkEntry(self.m_screen, show="*", text_font=self.text_bold)
        self.entry2.grid(row=3, column=3, columnspan=5, sticky="we")

        # Create Buttons
        self.btn1 = ctk.CTkButton(self.m_screen, text="Login", text_font=self.text_bold)
        self.btn1.grid(row=4, column=2, sticky="we")
        self.btn2 = ctk.CTkButton(self.m_screen, text="Cancel", text_font=self.text_bold)
        self.btn2.grid(row=4, column=7, sticky="we")

    def setup_grid(self):
        # set rows
        for row in range(self.rows):
            tk.Grid.rowconfigure(self.m_screen, row, weight=1)

        # set columns
        for col in range(self.cols):
            tk.Grid.columnconfigure(self.m_screen, col, weight=1)
