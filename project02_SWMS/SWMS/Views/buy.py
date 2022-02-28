import tkinter as tk
import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
import Controls.purchasesControls as PurControl


class Purchases:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols):
        self.m_screen = m_screen
        self.page_name = page_name
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.title = title

        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x) + 15}+{int(self.y) + 30}")
        self.m_screen.title(self.title)

        DB.opened_pages.append(self.page_name)
        TkServ.setup_grid(self.m_screen, self.width, self.height, self.grid_cols, self.grid_rows)

        # Set header
        self.header_lbl = tk.Label(self.m_screen, name="header_lbl", text="Purchases", font=("Ariel", 15, "bold"))
        self.header_lbl.grid(row=0, column=2, columnspan=5, sticky="w")

        # Create Labels
        self.total1_lbl = tk.Label(self.m_screen, text="TOTAL PRICE:", font=("Ariel", 13, "bold"))
        self.total1_lbl.grid(row=22, column=3, sticky="s", padx=10)
        self.total2_lbl = tk.Label(self.m_screen, name="total_price", text="0.0", font=("Ariel", 13, "bold"))
        self.total2_lbl.grid(row=23, column=3, sticky="we", padx=10)
        self.available_lbl = tk.Label(self.m_screen, name="available_products", text="Available Products",
                                      font=("Ariel", 12, "bold"))
        self.available_lbl.grid(row=9, column=0, sticky="we", padx=(0, 15))
        self.suppliers_lbl = tk.Label(self.m_screen, name="suppliers", text="Suppliers", font=("Ariel", 12, "bold"))
        self.suppliers_lbl.grid(row=9, column=3, sticky="we")

        # Create listbox with all the products that can be bought
        self.available_lb, self.available_items = TkServ.create_listbox(self.m_screen, "available_lb", row=10, column=0,
                                                                        width=35, height=25,
                                                                        rowspan=14, columnspan=1,
                                                                        data=[],
                                                                        padx=(10, 25), sticky="e")

        # Create dropdown with suppliers
        self.selected_supplier_var = tk.StringVar(self.m_screen)
        self.selected_supplier_var.set("None")
        self.drop_down_options = []
        for supplier in DB.suppliers:
            self.drop_down_options.append(f"{supplier.supp_id} | {supplier.supp_name}")
        self.selected_supplier = TkServ.create_drop_down(self.m_screen, self.selected_supplier_var,
                                                         self.drop_down_options,
                                                         lambda a: PurControl.on_supplier_change(self.m_screen,
                                                                                                 self.selected_supplier_var),
                                                         10, 3,
                                                         stick="we")

        # ----
        # Is there a way to set widget name on option menu ?
        # ----

        # Create transaction cart
        self.cart_lb, self.cart_items = TkServ.create_listbox(self.m_screen, "cart_lb", row=10, column=1, width=80,
                                                              height=25,
                                                              rowspan=14, columnspan=2, data=[])

        # Create buttons to manage the cart
        self.add_btn = tk.Button(self.m_screen, text="Add =>", name="add_to_cart_btn", font=("Arial", 12),
                                 bg="lightgreen",
                                 command=lambda: self.add_to_cart())
        self.add_btn.grid(row=9, column=1, sticky="w")
        self.rem_btn = tk.Button(self.m_screen, text="<= Remove", name="rem_item_from_cart_btn", font=("Arial", 12),
                                 bg="coral",
                                 command=lambda: self.rem_from_cart())
        self.rem_btn.grid(row=9, column=2, sticky="e", padx=(0, 35))
        self.clear_btn = tk.Button(self.m_screen, text="Clear", width=25, name="clear_cart_btn",
                                   font=("Arial", 12, "bold"),
                                   bg="red", fg="white",
                                   command=lambda: self.clear_cart())
        self.clear_btn.grid(row=24, column=1, columnspan=2, sticky="we", padx=(0, 35))
        self.buy_btn = tk.Button(self.m_screen, text="Buy", width=25, name="buy_cart_btn", font=("Arial", 12),
                                 bg="coral",
                                 command=lambda: self.buy())
        self.buy_btn.grid(row=24, column=3, sticky="we", padx=10)

        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def on_exit(self):
        DB.opened_pages.remove(self.page_name)
        self.m_screen.destroy()

    def add_to_cart(self):
        PurControl.add_item_to_cart(self.m_screen, self.cart_lb, self.available_lb, self.cart_items)

    def rem_from_cart(self):
        PurControl.rem_item_from_cart(self.m_screen, self.cart_lb, self.cart_items)

    def clear_cart(self):
        PurControl.clear_cart(self.m_screen, self.cart_lb, self.cart_items)

    def buy(self):
        PurControl.buy(self.m_screen, self.cart_lb, self.cart_items, self.available_items, self.selected_supplier_var)
