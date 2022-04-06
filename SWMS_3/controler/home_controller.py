import customtkinter as ctk

from model.entities.user import User
from model.service.logger import MyLogger
from view.components.warning_message import MyWarningMessage
from view.user_management_view import UserManagementView


class HomeController:
    def __init__(self, logger: MyLogger):
        self._logger = logger
        self._opened_views = []
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

    def user_mgmt(self, controller):
        if "user_mgmt" in self._opened_views:
            MyWarningMessage("User Management is already opened!")

        self._opened_views.append("user_mgmt")
        root = ctk.CTk()
        user_mgmt_view = UserManagementView(root, "User Management", controller)
        root.mainloop()
        self._opened_views.remove("user_mgmt")

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
