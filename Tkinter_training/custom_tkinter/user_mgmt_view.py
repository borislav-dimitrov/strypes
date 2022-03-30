import tkinter as tk
import customtkinter as ctk


class UserManagement:
    def __init__(self, m_screen, page_name, resolution: tuple, grid_rows=30, grid_cols=30):
        self.m_screen = m_screen
        self.page_name = page_name
        self.rows = grid_rows
        self.cols = grid_cols
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.colors = {"BLUE": "#1C94CF", "RED": "#871313", "LRED": "#823030", "DRED": "#731616"}
        self.txt_color = self.colors["BLUE"]
        self.m_screen.iconbitmap("main_ico.ico")

        # Set Geometry
        self.ww = resolution[0]
        self.wh = resolution[1]
        x = (self.m_screen.winfo_screenwidth() / 2) - (self.ww / 2)
        y = (self.m_screen.winfo_screenheight() / 2) - (self.wh / 2)
        self.m_screen.geometry("%dx%d+%d+%d" % (self.ww, self.wh, x, y))

        # Set Title
        self.m_screen.title(self.page_name)
        # Setup Grid
        self.setup_grid()

        # Create GUI
        # Create Header
        self.header = ctk.CTkLabel(self.m_screen, text=self.page_name, text_font=self.heading,
                                   text_color=self.txt_color)
        self.header.grid(row=0, column=0, columnspan=self.cols, sticky="we")

        # Create User Buttons
        self.create_btn = ctk.CTkButton(self.m_screen, text="Create User", text_font=self.text_bold)
        self.create_btn.grid(row=2, column=4, columnspan=2, sticky="we")
        self.edit_btn = ctk.CTkButton(self.m_screen, text="Update User", text_font=self.text_bold)
        self.edit_btn.grid(row=2, column=self.cols - 6, columnspan=2, sticky="we")

        self.create_btn_click()

    def setup_grid(self):
        # set rows
        for row in range(self.rows):
            tk.Grid.rowconfigure(self.m_screen, row, weight=1)

        # set columns
        for col in range(self.cols):
            tk.Grid.columnconfigure(self.m_screen, col, weight=1)

    def create_btn_click(self):
        self.header.configure(text="Create New User")

        # Create Labels
        uname_lbl = ctk.CTkLabel(self.m_screen, text="Username:", text_font=self.text_bold, text_color=self.txt_color)
        uname_lbl.grid(row=10, column=4, columnspan=2, sticky="e")
        pwd_lbl = ctk.CTkLabel(self.m_screen, text="Password:", text_font=self.text_bold, text_color=self.txt_color)
        pwd_lbl.grid(row=10, column=20, columnspan=2, sticky="e")
        type_lbl = ctk.CTkLabel(self.m_screen, text="Type:", text_font=self.text_bold, text_color=self.txt_color)
        type_lbl.grid(row=17, column=4, columnspan=2, sticky="e")
        status_lbl = ctk.CTkLabel(self.m_screen, text="Status:", text_font=self.text_bold, text_color=self.txt_color)
        status_lbl.grid(row=17, column=20, columnspan=2, sticky="e")

        # Create Inputs
        uname_entry = ctk.CTkEntry(self.m_screen, text_font=self.text_bold)
        uname_entry.grid(row=10, column=6, columnspan=4, sticky="we")
        pwd_entry = ctk.CTkEntry(self.m_screen, text_font=self.text_bold, show="*")
        pwd_entry.grid(row=10, column=22, columnspan=3, sticky="we")

        # Create Radio Buttons
        type_var = tk.StringVar()
        type_var.set("Operator")
        admin_rb = ctk.CTkRadioButton(self.m_screen, text="Administrator", variable=type_var, value="Administrator",
                                      text_font=self.text, text_color=self.txt_color)
        admin_rb.grid(row=16, column=6, columnspan=2, rowspan=2, sticky="sw", pady=(15, 0))
        operator_rb = ctk.CTkRadioButton(self.m_screen, text="Operator", variable=type_var, value="Operator",
                                         text_font=self.text, text_color=self.txt_color)
        operator_rb.grid(row=17, column=6, columnspan=2, rowspan=2, sticky="nw", pady=(0, 15))

        status_var = tk.StringVar()
        status_var.set("Enabled")
        enabled_rb = ctk.CTkRadioButton(self.m_screen, text="Enabled", variable=status_var, value="Enabled",
                                        text_font=self.text, text_color=self.txt_color)
        enabled_rb.grid(row=16, column=22, columnspan=2, rowspan=2, sticky="sw", pady=(15, 0))
        disabled_rb = ctk.CTkRadioButton(self.m_screen, text="Disabled", variable=type_var, value="Disabled",
                                         text_font=self.text, text_color=self.txt_color)
        disabled_rb.grid(row=17, column=22, columnspan=2, rowspan=2, sticky="nw", pady=(0, 15))

        # Create Buttons
        create_btn = ctk.CTkButton(self.m_screen, text="Create", text_font=self.text_bold)
        create_btn.grid(row=24, column=int(self.cols/2), columnspan=5, sticky="we")
