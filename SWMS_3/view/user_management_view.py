import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import view.utils.tkinter_utils as tkutil
from model.entities.user import User
from view.base_view import BaseView
from view.commands.user_commands.del_user_command import DelUserCommand
from view.commands.user_commands.show_create_user_command import ShowCreateUserCommand
from view.commands.user_commands.show_edit_user_command import ShowEditUserCommand
from view.components.item_list import ItemList

from view.commands.user_commands.close_users_view_command import CloseUsersViewCommand


class UserManagementView(BaseView):
    def __init__(self, parent, page_name, controller, curr_user, open_views, resolution: tuple = (1280, 728),
                 grid_rows=30, grid_cols=30, icon=None):
        super().__init__(parent, page_name, resolution, grid_rows, grid_cols, icon)
        self.parent = parent
        self.controller = controller
        self.curr_user = curr_user
        self.open_views = open_views

        # Users dropdown
        self.users_var = self.controller.users
        self.item_list = ItemList(self.parent, self.users_var, 7, 2, colspan=self.cols - 5)

        # Create Button
        self.create_btn = ttk.Button(self.parent, text="Create User", command=ShowCreateUserCommand(self.controller))
        self.create_btn.grid(row=20, column=5, columnspan=3, sticky="nsew")

        # Update Button
        self.edit_btn = ttk.Button(self.parent, text="Update User", command=ShowEditUserCommand(self.controller))
        self.edit_btn.grid(row=20, column=14, columnspan=3, sticky="nsew")

        # Delete Button
        self.del_btn = ttk.Button(self.parent, text="Delete User", command=DelUserCommand(self.controller))
        self.del_btn.grid(row=20, column=23, columnspan=3, sticky="nsew")

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", CloseUsersViewCommand(self.controller))

    def refresh(self):
        self.users_var = self.controller.users
        self.item_list.set_items(self.users_var)
