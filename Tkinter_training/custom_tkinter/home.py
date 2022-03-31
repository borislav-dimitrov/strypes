import tkinter as tk
import customtkinter as ctk
from window_menu import MyMenu
import theme_cfg as cfg


class MyHome:
    def __init__(self, m_screen, page_name, resolution: tuple, grid_rows=30, grid_cols=30):
        self.m_screen = m_screen
        self.page_name = page_name
        self.rows = grid_rows
        self.cols = grid_cols
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.colors = {"BLUE": "#1C94CF", "RED": "#871313", "LRED": "#823030", "DRED": "#731616"}
        self.MAIN_COLOR = cfg._MAIN_COLOR
        self.HOVER_COLOR = cfg._HOVER_COLOR
        self.TEXT_COLOR = cfg._TEXT_COLOR

        self.admin = True

        # Set Geometry
        self.ww = resolution[0]
        self.wh = resolution[1]
        x = (self.m_screen.winfo_screenwidth() / 2) - (self.ww / 2)
        y = (self.m_screen.winfo_screenheight() / 2) - (self.wh / 2)
        self.m_screen.geometry("%dx%d+%d+%d" % (self.ww, self.wh, x, y))

        # Set Title
        self.m_screen.title(self.page_name)

        # Set Icon
        self.m_screen.iconbitmap("main_ico.ico")

        # Setup Grid
        self.setup_grid()

        # Create GUI
        # Create Menu
        MyMenu(self.m_screen)
        # Create Header
        self.header = ctk.CTkLabel(self.m_screen, text=self.page_name, text_font=self.heading,
                                   text_color=self.TEXT_COLOR)
        self.header.grid(row=0, column=0, columnspan=self.cols, sticky="we")
        self.welcome = ctk.CTkLabel(self.m_screen, text="Welcome, user.", text_font=self.text_bold,
                                    text_color=self.TEXT_COLOR)
        self.welcome.grid(row=0, column=0, columnspan=2, sticky="we")

        # Logout Btn
        self.logout_btn = ctk.CTkButton(self.m_screen, text="Logout", text_font=self.text_bold, text_color="white",
                                        fg_color=self.colors["RED"], hover_color=self.colors["DRED"])
        self.logout_btn.grid(row=0, column=self.cols - 4, columnspan=3, sticky="e", padx=(0, 5))

        # Create User Buttons
        self.wh_btn = ctk.CTkButton(self.m_screen, text="Warehouses", text_font=self.text_bold,
                                    fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
        self.wh_btn.grid(row=9, column=4, rowspan=2, columnspan=2, sticky="nsew")
        self.pur_btn = ctk.CTkButton(self.m_screen, text="Purchases", text_font=self.text_bold,
                                     fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
        self.pur_btn.grid(row=9, column=10, rowspan=2, columnspan=2, sticky="nsew")
        self.sls_btn = ctk.CTkButton(self.m_screen, text="Sales", text_font=self.text_bold,
                                     fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
        self.sls_btn.grid(row=9, column=16, rowspan=2, columnspan=2, sticky="nsew")
        self.tr_btn = ctk.CTkButton(self.m_screen, text="Transactions", text_font=self.text_bold,
                                    fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
        self.tr_btn.grid(row=9, column=22, rowspan=2, columnspan=2, sticky="nsew")

        if self.admin:
            # Create Admin Buttons
            self.umgmt_btn = ctk.CTkButton(self.m_screen, text="User\nManagement", text_font=self.text_bold,
                                           fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
            self.umgmt_btn.grid(row=17, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.whmgmt_btn = ctk.CTkButton(self.m_screen, text="Warehouse\nManagement", text_font=self.text_bold,
                                            fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
            self.whmgmt_btn.grid(row=17, column=10, rowspan=2, columnspan=2, sticky="nsew")
            self.prmgmt_btn = ctk.CTkButton(self.m_screen, text="Product\nManagement", text_font=self.text_bold,
                                            fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
            self.prmgmt_btn.grid(row=17, column=16, rowspan=2, columnspan=2, sticky="nsew")
            self.spmgmt_btn = ctk.CTkButton(self.m_screen, text="Supplier\nManagement", text_font=self.text_bold,
                                            fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
            self.spmgmt_btn.grid(row=17, column=22, rowspan=2, columnspan=2, sticky="nsew")
            self.clmgmt_btn = ctk.CTkButton(self.m_screen, text="Client\nManagement", text_font=self.text_bold,
                                            fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
            self.clmgmt_btn.grid(row=21, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.invmgmt_btn = ctk.CTkButton(self.m_screen, text="Invoice\nManagement", text_font=self.text_bold,
                                             fg_color=self.MAIN_COLOR, hover_color=self.HOVER_COLOR)
            self.invmgmt_btn.grid(row=21, column=10, rowspan=2, columnspan=2, sticky="nsew")

    def setup_grid(self):
        # set rows
        for row in range(self.rows):
            tk.Grid.rowconfigure(self.m_screen, row, weight=1)

        # set columns
        for col in range(self.cols):
            tk.Grid.columnconfigure(self.m_screen, col, weight=1)
