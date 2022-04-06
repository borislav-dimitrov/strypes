import tkinter as tk

import customtkinter as ctk
import resources.theme_cfg as tcfg
import view.utils.tkinter_utils as tkutil
from controler.home_controller import HomeController
from controler.user_controller import UserController
from view.components.warning_message import MyWarningMessage


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
        self.MAIN_COLOR = tcfg._MAIN_COLOR
        self.HOVER_COLOR = tcfg._HOVER_COLOR

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
        self.header = ctk.CTkLabel(self.m_screen, text=self.page_name, text_font=self.heading,
                                   text_color=self.MAIN_COLOR)
        self.header.grid(row=0, column=1, columnspan=self.cols - 2, sticky="we")

        # Create Labels
        self.uname_lbl = ctk.CTkLabel(self.m_screen, text="Username:", text_font=self.text_bold,
                                      text_color=self.MAIN_COLOR)
        self.uname_lbl.grid(row=2, column=1, columnspan=2, sticky="we")
        self.pwd_lbl = ctk.CTkLabel(self.m_screen, text="Password:", text_font=self.text_bold,
                                    text_color=self.MAIN_COLOR)
        self.pwd_lbl.grid(row=3, column=1, columnspan=2, sticky="we")

        # Create Entry Fields
        self.uname_entry = ctk.CTkEntry(self.m_screen, text_font=self.text_bold)
        self.uname_entry.grid(row=2, column=3, columnspan=5, sticky="we")
        self.pwd_entry = ctk.CTkEntry(self.m_screen, show="*", text_font=self.text_bold)
        self.pwd_entry.grid(row=3, column=3, columnspan=5, sticky="we")

        # Create Buttons
        self.login_btn = ctk.CTkButton(self.m_screen, text="Login", text_font=self.text_bold, fg_color=self.MAIN_COLOR,
                                       hover_color=self.HOVER_COLOR, command=lambda: self.login())
        self.login_btn.grid(row=4, column=2, sticky="we")
        self.cancel_btn = ctk.CTkButton(self.m_screen, text="Cancel", text_font=self.text_bold,
                                        fg_color=self.MAIN_COLOR,
                                        hover_color=self.HOVER_COLOR, command=lambda: tkutil.close_all(self.m_screen))
        self.cancel_btn.grid(row=4, column=7, sticky="we")

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
            MyWarningMessage(msg)
