import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import view.utils.tkinter_utils as tkutil
from controler.main_controller import MainController
from controler.user_controller import UserController
from view.commands.login_commands.login_command import LoginCommand


class Login:
    def __init__(self, parent, page_name, resolution: tuple,
                 main_controller: MainController, grid_rows=30, grid_cols=30):
        self.controller: MainController = main_controller
        self.parent = parent
        self.page_name = page_name
        self.rows = grid_rows
        self.cols = grid_cols
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.colors = {"BLUE": "#1C94CF", "RED": "#871313", "LRED": "#823030", "DRED": "#731616"}

        # Set Geometry
        self.w = resolution[0]
        self.h = resolution[1]
        tkutil.center_window(self.parent, self.w, self.h)

        # Set Title
        self.parent.title(self.page_name)

        # Set Icon
        self.parent.iconbitmap("resources/icons/login_ico.ico")

        # Setup Grid
        tkutil.setup_grid(self.parent, self.rows, self.cols)

        # Create GUI
        # Create Header
        self.header = ttk.Label(self.parent, text=self.page_name, font=self.heading, anchor="center")
        self.header.grid(row=0, column=1, columnspan=self.cols - 2, sticky="we")

        # Create Labels
        self.uname_lbl = ttk.Label(self.parent, text="Username:", font=self.text_bold)
        self.uname_lbl.grid(row=2, column=1, columnspan=2, sticky="we")
        self.pwd_lbl = ttk.Label(self.parent, text="Password:", font=self.text_bold)
        self.pwd_lbl.grid(row=3, column=1, columnspan=2, sticky="we")

        # Create Entry Fields
        self.uname_entry = ttk.Entry(self.parent)
        self.uname_entry.grid(row=2, column=3, columnspan=5, sticky="we")
        self.pwd_entry = ttk.Entry(self.parent, show="*")
        self.pwd_entry.grid(row=3, column=3, columnspan=5, sticky="we")

        # Create Buttons
        self.login_btn = ttk.Button(self.parent, text="Login", command=LoginCommand(self.controller))
        self.login_btn.grid(row=4, rowspan=2, column=2, sticky="we")
        self.cancel_btn = ttk.Button(self.parent, text="Cancel", command=lambda: exit(0))
        self.cancel_btn.grid(row=4, rowspan=2, column=7, sticky="we")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", lambda: exit(0))
