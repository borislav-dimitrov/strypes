import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import view.utils.tkinter_utils as tkutil
from controler.user_controller import UserController
from view.base_view import BaseView


class UserManagementView(BaseView):
    def __init__(self, m_screen, page_name, controller: UserController, resolution: tuple = (1280, 728), grid_rows=30,
                 grid_cols=30,
                 icon=None):
        super().__init__(m_screen, page_name, resolution, grid_rows, grid_cols, icon)
        self.m_screen = m_screen
        self._controller = controller

        # Create GUI
        # Create User Buttons
        self.create_btn = ctk.CTkButton(self.m_screen, text="Create User", text_font=self.text_bold,
                                        fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                        command=lambda: self.create_user_click())
        self.create_btn.grid(row=2, column=4, columnspan=2, sticky="nsew")
        self.edit_btn = ctk.CTkButton(self.m_screen, text="Update User", text_font=self.text_bold,
                                      fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                      command=lambda: self.update_user_click())
        self.edit_btn.grid(row=2, column=self.cols - 6, columnspan=2, sticky="nsew")

        self._controller.create_user_btn_click(self.m_screen, self.header, self.text, self.text_bold, self._TEXT_COLOR,
                                               self._MAIN_COLOR, self._HOVER_COLOR, self.cols)
        # Exit protocol override
        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.default_exit())

    def create_user_click(self):
        # Clear Screen
        tkutil.clear_widgets(self.m_screen, [self.header, self.create_btn, self.edit_btn])

        # Create new GUI
        self._controller.create_user_btn_click(self.m_screen, self.header, self.text, self.text_bold, self._TEXT_COLOR,
                                               self._MAIN_COLOR, self._HOVER_COLOR, self.cols)

    def update_user_click(self):
        # Clear Screen
        tkutil.clear_widgets(self.m_screen, [self.header, self.create_btn, self.edit_btn])

        # Create new GUI
        self._controller.update_user_btn_click(self.m_screen, self.header, self.text, self.text_bold, self._TEXT_COLOR,
                                               self._MAIN_COLOR, self._HOVER_COLOR, self.cols)
