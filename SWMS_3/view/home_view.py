from tkinter import ttk

from view.base_view import BaseView

# Commands
from view.commands.exit_command import ExitCommand
from view.commands.home_view_commands.logout_command import LogoutCommand
from view.commands.home_view_commands.open_counterparty_management_command import OpenCounterpartyMgmtCommand
from view.commands.home_view_commands.open_product_management_command import OpenProductMgmtCommand
from view.commands.home_view_commands.open_purchases_command import OpenPurchasesCommand
from view.commands.home_view_commands.open_sales_command import OpenSalesCommand
from view.commands.home_view_commands.open_transactions_command import OpenTransactionsCommand
from view.commands.home_view_commands.open_user_management_command import OpenUserManagementCommand
from view.commands.home_view_commands.open_warehouses_command import OpenWarehousesCommand
from view.commands.home_view_commands.open_wh_management_command import OpenWhMgmtCommand


class HomeView(BaseView):
    def __init__(self, m_screen, page_name, controller, resolution: tuple = (1280, 728), grid_rows=30,
                 grid_cols=30,
                 icon=None):
        super().__init__(m_screen, page_name, resolution, grid_rows, grid_cols, icon)
        self.controller = controller

        # Create GUI
        self.welcome = ttk.Label(self.parent, text=f"Welcome, {self.controller.logged_user.name}.",
                                 font=self.text_bold)
        self.welcome.grid(row=0, column=1, columnspan=2, sticky="we")

        # region Buttons
        # Logout Button
        self.logout_btn = ttk.Button(self.parent, text="Logout", command=LogoutCommand(self.controller))
        self.logout_btn.grid(row=0, column=self.cols - 4, columnspan=3, sticky="e", padx=(0, 5))

        # Create Buttons
        self.wh_btn = ttk.Button(self.parent, text="Warehouses", command=OpenWarehousesCommand(self.controller))
        self.wh_btn.grid(row=9, column=4, rowspan=2, columnspan=2, sticky="nsew")
        self.pur_btn = ttk.Button(self.parent, text="Purchases", command=OpenPurchasesCommand(self.controller))
        self.pur_btn.grid(row=9, column=10, rowspan=2, columnspan=2, sticky="nsew")
        self.sls_btn = ttk.Button(self.parent, text="Sales", command=OpenSalesCommand(self.controller))
        self.sls_btn.grid(row=9, column=16, rowspan=2, columnspan=2, sticky="nsew")
        self.tr_btn = ttk.Button(self.parent, text="Transactions", command=OpenTransactionsCommand(self.controller))
        self.tr_btn.grid(row=9, column=22, rowspan=2, columnspan=2, sticky="nsew")

        if self.controller.logged_user.type == "Administrator":
            # Create Admin Buttons
            self.usr_mgmt_btn = ttk.Button(self.parent, text="User\nManagement",
                                           command=OpenUserManagementCommand(self.controller))
            self.usr_mgmt_btn.grid(row=17, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.wh_mgmt_btn = ttk.Button(self.parent, text="Warehouse\nManagement",
                                          command=OpenWhMgmtCommand(self.controller))
            self.wh_mgmt_btn.grid(row=17, column=10, rowspan=2, columnspan=2, sticky="nsew")
            self.pr_mgmt_btn = ttk.Button(self.parent, text="Product\nManagement",
                                          command=OpenProductMgmtCommand(self.controller))
            self.pr_mgmt_btn.grid(row=17, column=16, rowspan=2, columnspan=2, sticky="nsew")
            self.cpty_mgmt_btn = ttk.Button(self.parent, text="Counterparty\nManagement",
                                            command=OpenCounterpartyMgmtCommand(self.controller))
            self.cpty_mgmt_btn.grid(row=17, column=22, rowspan=2, columnspan=2, sticky="nsew")
        # endregion

        # Exit protocol override
        self.parent.protocol("WM_DELETE_WINDOW", ExitCommand(self.controller))
