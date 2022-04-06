import tkinter as tk
from tkinter import ttk

import view.utils.tkinter_utils as tkutil
from controler.user_controller import UserController
from view.base_view import BaseView
from view.commands.users.show_add_user_command import ShowAddUserCommand
from view.components.item_list import ItemList


class UserManagementView(BaseView):
    def __init__(self, m_screen, page_name, controller: UserController, resolution: tuple = (1280, 728), grid_rows=30,
                 grid_cols=30, icon=None):
        super().__init__(m_screen, page_name, resolution, grid_rows, grid_cols, icon)
        self.m_screen = m_screen
        self.controller = controller
        self.show_add_user_command = ShowAddUserCommand(self.controller)
        self.controller.view = self

        # Create GUI

        # Users dropdown
        users_var = self.controller.users
        users = ItemList(self.m_screen, users_var, 7, 2, colspan=self.cols - 5)

        # Create Button
        self.create_btn = ttk.Button(self.m_screen, text="Create User", command=lambda: self.show_add_user_command)
        self.create_btn.grid(row=20, column=5, columnspan=3, sticky="nsew")

        # Update Button
        self.edit_btn = ttk.Button(self.m_screen, text="Update User", command=lambda: print("edit"))
        self.edit_btn.grid(row=20, column=14, columnspan=3, sticky="nsew")

        # Delete Button
        self.del_btn = ttk.Button(self.m_screen, text="Delete User", command=lambda: print("delete"))
        self.del_btn.grid(row=20, column=23, columnspan=3, sticky="nsew")

        # Exit protocol override
        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.default_exit())
