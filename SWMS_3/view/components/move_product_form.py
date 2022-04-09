import tkinter as tk
from tkinter import ttk
import view.utils.tkinter_utils as tkutil


class MoveProductForm(tk.Toplevel):
    def __init__(self, parent, controller, chosen_product, current_warehouse, width=600, height=400):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.chosen_product = chosen_product
        self.current_wh = current_warehouse

        self.frame = ttk.Frame(self, padding="30 30 30 30")
        self.title(f"Move Product {self.chosen_product.name}")
        self.frame.grid(row=0, column=0, sticky="nsew")
        tkutil.center_window(self, width, height)
        tkutil.setup_grid(self, 6, 3)

        # Label
        label = ttk.Label(self, text="Chose where to move the product.", font=("Arial", 12, "bold"), anchor="center")
        label.grid(row=1, column=1, sticky="swe")

        # Warehouses List
        self.warehouses_list = ["None", *self.controller.filtered_warehouses(self.current_wh)]
        self.move_to_var = tk.StringVar()
        self.move_to_var.set(self.warehouses_list[0])
        self.warehouses_dropdown = tk.OptionMenu(self, self.move_to_var, *self.warehouses_list)
        self.warehouses_dropdown.grid(row=2, column=1, sticky="nwe")

        # Move Button
        self.move_btn = ttk.Button(self, text="Move",
                                   command=lambda: self.move())
        self.move_btn.grid(row=3, column=1)

        # capture visibility
        self.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.transient(self.parent)
        self.wait_visibility()
        self.grab_set()
        self.wait_window()

    def dismiss(self):
        self.grab_release()
        self.destroy()

    def move(self):
        result = self.controller.move_product(self.chosen_product, self.move_to_var)
        if result == "Ok":
            self.dismiss()
