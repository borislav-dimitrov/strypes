import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
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
        # Create GUI
        self.welcome = ctk.CTkLabel(self.m_screen, text=f"Welcome, {self._controller._logged_user.name}.",
                                    text_font=self.text_bold, text_color=self._TEXT_COLOR)
        self.welcome.grid(row=0, column=0, columnspan=2, sticky="we")

        # region Buttons
        # Logout Button
        self.logout_btn = ctk.CTkButton(self.m_screen, text="Logout", text_font=self.text_bold, text_color="white",
                                        fg_color=self.colors["RED"], hover_color=self.colors["DRED"],
                                        command=lambda: self.logout())
        self.logout_btn.grid(row=0, column=self.cols - 4, columnspan=3, sticky="e", padx=(0, 5))

        # Create Buttons
        self.wh_btn = ctk.CTkButton(self.m_screen, text="Warehouses", text_font=self.text_bold,
                                    fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                    command=lambda: self._controller.warehouses())
        self.wh_btn.grid(row=9, column=4, rowspan=2, columnspan=2, sticky="nsew")
        self.pur_btn = ctk.CTkButton(self.m_screen, text="Purchases", text_font=self.text_bold,
                                     fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                     command=lambda: self._controller.purchases())
        self.pur_btn.grid(row=9, column=10, rowspan=2, columnspan=2, sticky="nsew")
        self.sls_btn = ctk.CTkButton(self.m_screen, text="Sales", text_font=self.text_bold,
                                     fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                     command=lambda: self._controller.sales())
        self.sls_btn.grid(row=9, column=16, rowspan=2, columnspan=2, sticky="nsew")
        self.tr_btn = ctk.CTkButton(self.m_screen, text="Transactions", text_font=self.text_bold,
                                    fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                    command=lambda: self._controller.transactions())
        self.tr_btn.grid(row=9, column=22, rowspan=2, columnspan=2, sticky="nsew")

        if self._controller._logged_user.type == "Administrator":
            # Create Admin Buttons
            self.umgmt_btn = ctk.CTkButton(self.m_screen, text="User\nManagement", text_font=self.text_bold,
                                           fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                           command=lambda: self._controller.user_mgmt(self._systems["user_controller"]))
            self.umgmt_btn.grid(row=17, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.whmgmt_btn = ctk.CTkButton(self.m_screen, text="Warehouse\nManagement", text_font=self.text_bold,
                                            fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                            command=lambda: self._controller.warehouse_mgmt())
            self.whmgmt_btn.grid(row=17, column=10, rowspan=2, columnspan=2, sticky="nsew")
            self.prmgmt_btn = ctk.CTkButton(self.m_screen, text="Product\nManagement", text_font=self.text_bold,
                                            fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                            command=lambda: self._controller.product_mgmt())
            self.prmgmt_btn.grid(row=17, column=16, rowspan=2, columnspan=2, sticky="nsew")
            self.spmgmt_btn = ctk.CTkButton(self.m_screen, text="Supplier\nManagement", text_font=self.text_bold,
                                            fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                            command=lambda: self._controller.supplier_mgmt())
            self.spmgmt_btn.grid(row=17, column=22, rowspan=2, columnspan=2, sticky="nsew")
            self.clmgmt_btn = ctk.CTkButton(self.m_screen, text="Client\nManagement", text_font=self.text_bold,
                                            fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                            command=lambda: self._controller.client_mgmt())
            self.clmgmt_btn.grid(row=21, column=4, rowspan=2, columnspan=2, sticky="nsew")
            self.invmgmt_btn = ctk.CTkButton(self.m_screen, text="Transaction\nManagement", text_font=self.text_bold,
                                             fg_color=self._MAIN_COLOR, hover_color=self._HOVER_COLOR,
                                             command=lambda: self._controller.transaction_mgmt())
            self.invmgmt_btn.grid(row=21, column=10, rowspan=2, columnspan=2, sticky="nsew")
        # endregion

        # Exit protocol override
        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: tkutil.close_all(self.m_screen, self._systems))

    def logout(self):
        self._controller._logging_out = True
        self._controller._logged_user = None
        tkutil.close_win(self.m_screen)
