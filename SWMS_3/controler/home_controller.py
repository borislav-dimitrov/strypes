import tkinter as tk
from tkinter import messagebox

from model.entities.user import User
from model.service.logger import MyLogger
from view.user_management_view import UserManagementView
from view.utils.open_views_track import _OPENED_VIEWS


class HomeController:
    def __init__(self, logger: MyLogger):
        self.view = None
        self._logger = logger
        self._logged_user: User = None
        self._logging_out = False

    @staticmethod
    def test():
        print("test")

    def warehouses(self):
        pass

    def purchases(self):
        pass

    def sales(self):
        pass

    def transactions(self):
        pass

    def user_mgmt(self, controller) -> None:
        """Static method called from home view with the specific controller for each page"""
        page_name = "User Management"
        if page_name in _OPENED_VIEWS:
            messagebox.showwarning("Warning!", f"Page {page_name} is already opened!")
            return

        _OPENED_VIEWS.append(page_name)
        root = tk.Toplevel()
        user_mgmt_view = UserManagementView(root, page_name, controller, self._logged_user)
        root.mainloop()

    def warehouse_mgmt(self):
        pass

    def product_mgmt(self):
        pass

    def supplier_mgmt(self):
        pass

    def client_mgmt(self):
        pass

    def transaction_mgmt(self):
        pass
