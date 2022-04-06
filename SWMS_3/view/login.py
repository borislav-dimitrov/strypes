import tkinter as tk
from tkinter import ttk

import view.utils.tkinter_utils as tkutil
from controler.home_controller import HomeController
from controler.user_controller import UserController


class Login:
    def __init__(self, m_screen, page_name, resolution: tuple, usr_controller: UserController,
                 home_controller: HomeController, grid_rows=30, grid_cols=30):
        self._usr_controller = usr_controller
        self._home_controller = home_controller
        self.m_screen = m_screen
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
        tkutil.center_window(self.m_screen, self.w, self.h)

        # Set Title
        self.m_screen.title(self.page_name)

        # Set Icon
        self.m_screen.iconbitmap("resources/icons/login_ico.ico")

        # Setup Grid
        self.setup_grid()

        # Create GUI
        # Create Header
        self.header = ttk.Label(self.m_screen, text=self.page_name, font=self.heading, anchor="center")
        self.header.grid(row=0, column=1, columnspan=self.cols - 2, sticky="we")

        # Create Labels
        self.uname_lbl = ttk.Label(self.m_screen, text="Username:", font=self.text_bold)
        self.uname_lbl.grid(row=2, column=1, columnspan=2, sticky="we")
        self.pwd_lbl = ttk.Label(self.m_screen, text="Password:", font=self.text_bold)
        self.pwd_lbl.grid(row=3, column=1, columnspan=2, sticky="we")

        # Create Entry Fields
        self.uname_entry = ttk.Entry(self.m_screen)
        self.uname_entry.grid(row=2, column=3, columnspan=5, sticky="we")
        self.pwd_entry = ttk.Entry(self.m_screen, show="*")
        self.pwd_entry.grid(row=3, column=3, columnspan=5, sticky="we")

        # Create Buttons
        self.login_btn = ttk.Button(self.m_screen, text="Login", command=lambda: self.login())
        self.login_btn.grid(row=4, rowspan=2, column=2, sticky="we")
        self.cancel_btn = ttk.Button(self.m_screen, text="Cancel", command=lambda: tkutil.close_all(self.m_screen))
        self.cancel_btn.grid(row=4, rowspan=2, column=7, sticky="we")

        # Exit protocol override
        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: exit(0))

    def setup_grid(self):
        # set rows
        for row in range(self.rows):
            tk.Grid.rowconfigure(self.m_screen, row, weight=1)

        # set columns
        for col in range(self.cols):
            tk.Grid.columnconfigure(self.m_screen, col, weight=1)

    def login(self):
        uname = self.uname_entry.get()
        pwd = self.pwd_entry.get()
        login_state, msg, user = self._usr_controller.login(uname, pwd)
        if login_state:
            self._home_controller._logged_user = user
            self.m_screen.destroy()
        else:
            # TODO warning
            print(msg)
