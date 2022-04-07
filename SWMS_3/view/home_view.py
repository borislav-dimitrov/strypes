import tkinter as tk
from tkinter import ttk
import view.utils.tkinter_utils as tkutil

from controler.home_controller import HomeController
from view.base_view import BaseView


class HomeView(BaseView):
    def __init__(self, m_screen, page_name, systems: dict, resolution: tuple = (1280, 728), grid_rows=30,
                 grid_cols=30,
                 icon=None):
        super().__init__(m_screen, page_name, resolution, grid_rows, grid_cols, icon)
        self._controller: HomeController = systems["home_controller"]
        self._systems = systems
        self._controller.view = self

        # Create GUI
        self.welcome = ttk.Label(self.parent, text=f"Welcome, {self._controller._logged_user.name}.",
                                 font=self.text_bold)
        self.welcome.grid(row=0, column=0, columnspan=2, sticky="we")

        # region Buttons
        # Logout Button
        self.logout_btn = ttk.Button(self.parent, text="Logout", command=lambda: self.logout())
        self.logout_btn.grid(row=0, column=self.cols - 4, columnspan=3, sticky="e", padx=(0, 5))

        # Create Buttons
        self.wh_btn = ttk.Button(self.parent, text="Warehouses", command=lambda: self._controller.warehouses())
        self.wh_btn.grid(row=9, column=4, rowspan=2, columnspan=2, sticky="nsew")
        self.pur_btn = ttk.Button(self.parent, text="Purchases", command=lambda: self._controller.purchases())
        self.pur_btn.grid(row=9, column=10, rowspan=2, columnspan=2, sticky="nsew")
        self.sls_btn = ttk.Button(self.parent, text="Sales", command=lambda: self._controller.sales())
        self.sls_btn.grid(row=9, column=16, rowspan=2, columnspan=2, sticky="nsew")
        self.tr_btn = ttk.Button(self.parent, text="Transactions", command=lambda: self._controller.transactions())
        self.tr_btn.grid(row=9, column=22, rowspan=2, columnspan=2, sticky="nsew")

        if self._controller._logged_user.type == "Administrator":
            # Create Admin Buttons
            self.umgmt_btn = ttk.Button(self.parent, text="User\nManagement",
                                        command=lambda: self._controller.user_mgmt(self._systems["user_controller"]))
            self.umgmt_btn.grid(row=17, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.whmgmt_btn = ttk.Button(self.parent, text="Warehouse\nManagement",
                                         command=lambda: self._controller.warehouse_mgmt(
                                             self._systems["warehousing_controller"]))
            self.whmgmt_btn.grid(row=17, column=10, rowspan=2, columnspan=2, sticky="nsew")
            self.prmgmt_btn = ttk.Button(self.parent, text="Product\nManagement",
                                         command=lambda: self._controller.product_mgmt())
            self.prmgmt_btn.grid(row=17, column=16, rowspan=2, columnspan=2, sticky="nsew")
            self.spmgmt_btn = ttk.Button(self.parent, text="Supplier\nManagement",
                                         command=lambda: self._controller.supplier_mgmt())
            self.spmgmt_btn.grid(row=17, column=22, rowspan=2, columnspan=2, sticky="nsew")
            self.clmgmt_btn = ttk.Button(self.parent, text="Client\nManagement",
                                         command=lambda: self._controller.client_mgmt())
            self.clmgmt_btn.grid(row=21, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.invmgmt_btn = ttk.Button(self.parent, text="Transaction\nManagement",
                                          command=lambda: self._controller.transaction_mgmt())
            self.invmgmt_btn.grid(row=21, column=10, rowspan=2, columnspan=2, sticky="nsew")
        # endregion

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", lambda: tkutil.close_all(self.parent, self._systems))

    def logout(self):
        self._controller._logging_out = True
        self._controller._logged_user = None
        tkutil.close_win(self.parent)
