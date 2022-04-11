import tkinter as tk
from tkinter import messagebox
from datetime import datetime

# Config file
import resources.config as cfg

# Controllers
from controler.sales_controller import SalesController
from controler.user_controller import UserController
from controler.warehousing_controller import WarehousingController

# Repositories
from model.dao.pdf_maker import PdfMaker
from model.dao.repositories.generic_repo import GenericRepository
from model.dao.repositories.invoice_repo import InvoiceRepository

# Other DAO's
from model.dao.id_generator_int import IdGeneratorInt
from model.dao.password_manager import PasswordManager

# Entities
from model.entities.user import User
from model.service.logger import MyLogger

# Modules / Services
from model.service.modules.sales_module import SalesModule
from model.service.modules.users_module import UserModule
from model.service.modules.warehousing_module import WarehousingModule

# Views
from view.purchases_view import PurchasesView
from view.sales_view import SalesView
from view.transactions_view import TransactionsView
from view.warehouses_view import WarehousesView
from view.user_management_view import UserManagementView
from view.warehouse_management_view import WarehouseManagementView
from view.product_management_view import ProductManagementView
from view.counterparty_management_view import CounterpartyManagementView


class MainController:
    def __init__(self):
        self.view = None
        self.logger = None
        self.pdf_maker = None
        self.logged_user: User = None
        self.logging_out = False
        self.user_controller: UserController = None
        self.warehousing_controller: WarehousingController = None
        self.sales_controller: SalesController = None
        self.opened_views = []

    def startup(self):
        """Initialize all repositories, modules, etc."""
        # OTHER
        logger = MyLogger(cfg.LOG_ENABLED, cfg.DEFAULT_LOG_FILE, cfg.LOG_LEVEL, cfg.REWRITE_LOG_ON_STARTUP)
        self.logger = logger
        self.pdf_maker = PdfMaker()
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
        sales_module = SalesModule(cpty_repo, tr_repo, inv_repo, logger, self.pdf_maker)

        # CONTROLLERS
        self.user_controller = UserController(user_module, logger)
        self.warehousing_controller = WarehousingController(warehousing_module, logger)
        self.sales_controller = SalesController(sales_module, self.warehousing_controller, logger)

        # Load data from json files
        self.user_controller.load()
        self.warehousing_controller.load_all()
        self.sales_controller.load_all()

    def before_exit(self):
        """Execute before exit"""
        if self.logged_user is not None:
            self.logger.log(__file__, f"User {self.logged_user.name} has logged out.", "INFO")
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
            self.logged_user.last_login = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
            self.logger.log(__file__, f"User {self.logged_user.name} has logged in.", "INFO")
            self.view.parent.destroy()
        else:
            messagebox.showerror("Warning!", msg)

    def logout(self):
        self.logger.log(__file__, f"User {self.logged_user.name} has logged out.", "INFO")
        self.logging_out = True
        self.logged_user = None
        self.view.parent.destroy()

    # region Manage Views
    def warehouses(self):
        """Initialize Warehouses View"""
        page_name = "Warehouses"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        warehouses_view = WarehousesView(root, page_name, self.warehousing_controller, self.opened_views)
        self.warehousing_controller.warehouses_view = warehouses_view
        root.mainloop()

    def purchases(self):
        """Initialize Purchases View"""
        page_name = "Purchases"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        pur_view = PurchasesView(root, page_name, self.sales_controller, self.opened_views)
        self.sales_controller.pur_view = pur_view
        root.mainloop()

    def sales(self):
        """Initialize Sales View"""
        page_name = "Sales"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        sales_view = SalesView(root, page_name, self.sales_controller, self.opened_views)
        self.sales_controller.sales_view = sales_view
        root.mainloop()

    def transactions(self):
        """Initialize Transactions View"""
        page_name = "Transactions"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        tr_view = TransactionsView(root, page_name, self.sales_controller, self.opened_views)
        self.sales_controller.tr_view = tr_view
        root.mainloop()

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

    def counterparty_mgmt(self):
        """Initialize Counterparty Management View"""
        page_name = "Counterparty Management"
        if page_name in self.opened_views:
            messagebox.showerror("Warning!", f"Page {page_name} is already opened!")
            return

        self.opened_views.append(page_name)
        root = tk.Toplevel()
        cpty_mgmt_view = CounterpartyManagementView(root, page_name, self.sales_controller, self.opened_views)
        self.sales_controller.counterparty_view = cpty_mgmt_view
        root.mainloop()

    # endregion
