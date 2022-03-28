import tkinter as tk
from tkinter import ttk
import Model.DataBase.my_db as db
import Helpers.tk_helpers as tkhlp


class MyHome:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols):
        self.m_screen = m_screen
        self.page_name = page_name
        self.title = title
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")
        self.logging_out = False
        self.exiting = False

        # region Styles

        # region Buttons
        self.accept_btn_style = ttk.Style()
        self.accept_btn_style.theme_use("alt")

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.theme_use("alt")

        self.normal_btn_style = ttk.Style()
        self.normal_btn_style.theme_use("alt")

        self.accept_btn_style.configure('Green.TButton', background='#98ff61', foreground='black', width=20,
                                        borderwidth=1, font=self.text_bold,
                                        focusthickness=5, focuscolor='red')
        self.accept_btn_style.map('Green.TButton', background=[('active', '#98ff61')])

        self.cancel_btn_style.configure('Red.TButton', background='red', foreground='black', width=10, borderwidth=1,
                                        font=self.text_bold,
                                        focusthickness=5, focuscolor='#98ff61')
        self.cancel_btn_style.map('Red.TButton', background=[('active', 'red')])

        self.normal_btn_style.configure('Normal.TButton', background='#4bb8ff', foreground='black', width=15,
                                        borderwidth=1, font=self.text_bold,
                                        focusthickness=5, focuscolor='#98ff61')
        self.normal_btn_style.map('Normal.TButton', background=[('active', '#4bb8ff')])
        # endregion

        # endregion

        self.m_screen.iconbitmap("./Resources/images/main_ico.ico")

        # Set Geometry
        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.m_screen.resizable(False, False)
        # Set Title
        self.m_screen.title(title)
        # Setup Grid
        tkhlp.setup_grid(self.m_screen, self.grid_rows, self.grid_cols, self.height, self.width)
        # Create GUI

        self.bg_img = tk.PhotoImage(file="./Resources/images/home/home2.png")
        self.canvas = tk.Canvas(self.m_screen, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, columnspan=self.grid_cols, rowspan=self.grid_rows, sticky="nesw")
        # Draw BG
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        # Draw Header
        self.canvas.create_text(self.width / 2, 50, text=self.page_name, font=self.heading, fill="white")
        # Draw Labels
        self.canvas.create_text(100, 50, text=f"Hello, {db.curr_user.user_name}.", font=self.text_bold, fill="white")

        # Logout Btn
        self.logout_btn = ttk.Button(self.m_screen, text="Logout", style="Red.TButton", command=lambda: self.logout())
        self.logout_btn.grid(row=1, column=self.grid_cols - 4, columnspan=3, sticky="e", padx=(0, 5))

        # Create User Buttons
        self.wh_btn = ttk.Button(self.m_screen, text="Warehouses", style="Normal.TButton",
                                 command=lambda: self.warehouses())
        self.wh_btn.grid(row=9, column=4, rowspan=2, columnspan=15, sticky="wns")
        self.pur_btn = ttk.Button(self.m_screen, text="Purchases", style="Normal.TButton",
                                  command=lambda: self.purchases())
        self.pur_btn.grid(row=9, column=10, rowspan=2, columnspan=15, sticky="wns")
        self.sls_btn = ttk.Button(self.m_screen, text="Sales", style="Normal.TButton", command=lambda: self.sales())
        self.sls_btn.grid(row=9, column=16, rowspan=2, columnspan=15, sticky="wns")
        self.tr_btn = ttk.Button(self.m_screen, text="Transactions", style="Normal.TButton",
                                 command=lambda: self.transactions())
        self.tr_btn.grid(row=9, column=22, rowspan=2, columnspan=15, sticky="wns")

        if db.curr_user.user_type.lower() == "administrator":
            # Create Admin Buttons
            self.umgmt_btn = ttk.Button(self.m_screen, text="User\nManagement", style="Normal.TButton",
                                        command=lambda: self.user_mgmt())
            self.umgmt_btn.grid(row=17, column=4, rowspan=2, columnspan=15, sticky="wns")
            self.whmgmt_btn = ttk.Button(self.m_screen, text="Warehouse\nManagement", style="Normal.TButton",
                                         command=lambda: self.warehouse_mgmt())
            self.whmgmt_btn.grid(row=17, column=10, rowspan=2, columnspan=15, sticky="wns")
            self.prmgmt_btn = ttk.Button(self.m_screen, text="Product\nManagement", style="Normal.TButton",
                                         command=lambda: self.product_mgmt())
            self.prmgmt_btn.grid(row=17, column=16, rowspan=2, columnspan=15, sticky="wns")
            self.supplmgmt_btn = ttk.Button(self.m_screen, text="Supplier\nManagement", style="Normal.TButton",
                                            command=lambda: self.supplier_mgmt())
            self.supplmgmt_btn.grid(row=17, column=22, rowspan=2, columnspan=15, sticky="wns")
            self.climgmt_btn = ttk.Button(self.m_screen, text="Client\nManagement", style="Normal.TButton",
                                          command=lambda: self.client_mgmt())
            self.climgmt_btn.grid(row=21, column=4, rowspan=2, columnspan=15, sticky="wns")
            self.invmgmt_btn = ttk.Button(self.m_screen, text="Invoice\nManagement", style="Normal.TButton",
                                          command=lambda: self.invoice_mgmt())
            self.invmgmt_btn.grid(row=21, column=10, rowspan=2, columnspan=15, sticky="wns")

        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def on_exit(self):
        self.exiting = True
        self.m_screen.destroy()

    def logout(self):
        self.logging_out = True
        self.m_screen.destroy()

    def warehouses(self):
        db.opened_pages.append("warehouses")
        if "warehouses" in db.opened_pages:
            # TODO tkinter message
            tkhlp.create_custom_msg(self.m_screen, "Warning!", "Warehouses window is already opened!")
            print("warehouses already opened")
            return

    def purchases(self):
        print("purchases")

    def sales(self):
        print("sales")

    def transactions(self):
        print("transactions")

    def user_mgmt(self):
        print("user_mgmt")

    def warehouse_mgmt(self):
        print("warehouse mgmt")

    def product_mgmt(self):
        print("product mgmt")

    def supplier_mgmt(self):
        print("suppl mgmt")

    def client_mgmt(self):
        print("client mgmt")

    def invoice_mgmt(self):
        print("invoice mgmt")
