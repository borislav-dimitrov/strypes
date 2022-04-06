import customtkinter as ctk

from model.entities.user import User
from model.service.logger import MyLogger
from view.components.warning_message import MyWarningMessage
from view.user_management_view import UserManagementView
from view.utils.open_views_track import _OPENED_VIEWS


class HomeController:
    def __init__(self, logger: MyLogger):
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

    @staticmethod
    def user_mgmt(controller) -> None:
        """Static method called from home view with the specific controller for each page"""
        page_name = "User Management"
        if page_name in _OPENED_VIEWS:
            MyWarningMessage("User Management is already opened!")

        _OPENED_VIEWS.append(page_name)
        root = ctk.CTk()
        user_mgmt_view = UserManagementView(root, page_name, controller)
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
