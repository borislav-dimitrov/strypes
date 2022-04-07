import tkinter as tk
from tkinter import messagebox

import resources.config as cfg

from controler.sales_controller import SalesController
from controler.user_controller import UserController
from controler.warehousing_controller import WarehousingController

from model.dao.id_generator_int import IdGeneratorInt
from model.dao.password_manager import PasswordManager

from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.invoice_repo import InvoiceRepository

from model.entities.user import User
from model.service.logger import MyLogger

from model.service.modules.sales_module import SalesModule
from model.service.modules.users_module import UserModule
from model.service.modules.warehousing_module import WarehousingModule

from view.user_management_view import UserManagementView
from view.warehouse_management_view import WarehouseManagementView
from view.product_management_view import ProductManagementView


class MainController:
    def __init__(self):
        self.view = None
        self.logger = None
        self.logged_user: User = None
        self.logging_out = False
        self.user_controller = None
        self.warehousing_controller = None
        self.sales_controller = None
        self.opened_views = []

    def startup(self):
        """Initialize all repositories, modules, etc."""
        # OTHER
        logger = MyLogger(cfg.LOG_ENABLED, cfg.DEFAULT_LOG_FILE, cfg.LOG_LEVEL, cfg.REWRITE_LOG_ON_STARTUP)
        self.logger = logger

        # REPOSITORIES
        usr_id_seq = IdGeneratorInt()
        usr_repo = GenericRepository(usr_id_seq, logger)

        wh_id_seq = IdGeneratorInt()
        wh_repo = GenericRepository(wh_id_seq, logger)

        pr_id_seq = IdGeneratorInt()
        pr_repo = GenericRepository(pr_id_seq, logger)

        cpty_id_seq = IdGeneratorInt()
        cpty_repo = GenericRepository(cpty_id_seq, logger)

        tr_id_seq = IdGeneratorInt()
        tr_repo = GenericRepository(tr_id_seq, logger)

        inv_id_seq = IdGeneratorInt()
        inv_repo = InvoiceRepository(inv_id_seq, logger)

        # MODULES
        user_module = UserModule(usr_repo, PasswordManager(), logger)
        warehousing_module = WarehousingModule(pr_repo, wh_repo, logger)
        sales_module = SalesModule(cpty_repo, tr_repo, inv_repo, logger)

        # CONTROLLERS
        self.user_controller = UserController(user_module, logger)
        self.warehousing_controller = WarehousingController(warehousing_module, logger)
        self.sales_controller = SalesController(sales_module, logger)

        # Load data from json files
        self.user_controller.load()
        self.warehousing_controller.load_all()
        self.sales_controller.load_all()

    def before_exit(self):
        """Execute before exit"""
        self.user_controller.save()
        self.warehousing_controller.save_all()
        self.sales_controller.save_all()

    def exit(self):
        self.before_exit()
        exit(0)

    def login(self):
        uname = self.view.uname_entry.get()
        pwd = self.view.pwd_entry.get()

        login_state, msg, user = self.user_controller.login(uname, pwd)

        if login_state:
            self.logged_user = user
            self.view.parent.destroy()
        else:
            messagebox.showerror("Warning!", msg)

    def logout(self):
        self.logging_out = True
        self.logged_user = None
        self.view.parent.destroy()

    # region Manage Views
    def warehouses(self):
        pass

    def purchases(self):
        pass

    def sales(self):
        pass

    def transactions(self):
        pass

    def user_mgmt(self) -> None:
        """Initialize User Management View"""
        page_name = "User Management"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        user_mgmt_view = UserManagementView(root, page_name, self.user_controller, self.logged_user, self.opened_views)
        self.user_controller.view = user_mgmt_view
        root.mainloop()

    def warehouse_mgmt(self):
        """Initialize Warehouse Management View"""
        page_name = "Warehouse Management"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        whs_mgmt_view = WarehouseManagementView(root, page_name, self.warehousing_controller, self.opened_views)
        self.warehousing_controller.wh_management_view = whs_mgmt_view
        root.mainloop()

    def product_mgmt(self):
        """Initialize Product Management View"""
        page_name = "Product Management"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        product_mgmt_view = ProductManagementView(root, page_name, self.warehousing_controller, self.opened_views)
        self.warehousing_controller.pr_management_view = product_mgmt_view
        root.mainloop()

    def supplier_mgmt(self):
        pass

    def client_mgmt(self):
        pass

    def transaction_mgmt(self):
        pass
    # endregion
