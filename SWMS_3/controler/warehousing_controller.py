from tkinter import messagebox

from model.entities.product import Product
from model.entities.warehouse import Warehouse
from model.service.logger import MyLogger
from model.service.modules.warehousing_module import WarehousingModule
from view.components.item_form import ItemForm


class WarehousingController:
    def __init__(self, warehousing_module: WarehousingModule, logger: MyLogger):
        self.module = warehousing_module
        self.logger = logger
        self.wh_management_view = None
        self.pr_management_view = None
        self.warehousing_view = None

    @property
    def warehouses(self):
        return self.module.warehouses

    @property
    def products(self):
        return self.module.products

    # region Load/Save/Reload
    def load_all(self):
        self.module.load_all()

    def save_all(self):
        self.module.save_all()

    def reload(self):
        self.save_all()
        self.load_all()

    # endregion

    # region FIND
    def find_wh_by_id(self, id_):
        return self.module.find_wh_by_id(id_)

    def products_in_wh_count(self, wh_id) -> int:
        warehouse = self.find_wh_by_id(wh_id)
        total = 0
        for product in warehouse.products:
            total += product.quantity
        return total

    # endregion

    # region CRUD

    # region Warehouse Management
    def create_warehouse(self, name, type_, capacity, products, status):
        result = self.module.create_wh(name, type_, capacity, [], status)
        if isinstance(result, Warehouse):
            self.reload()
            self.wh_management_view.refresh()
            messagebox.showinfo("Info!", f"Warehouse {result.name} has been created successfully!",
                                parent=self.wh_management_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.wh_management_view.parent)
        return result

    def update_warehouse(self, name, type_, capacity, products, status, id_):
        result = self.module.update_warehouse(self.module.find_wh_by_id(id_), name, type_, capacity, products, status)
        if isinstance(result, Warehouse):
            self.reload()
            self.wh_management_view.refresh()
            messagebox.showinfo("Info!", f"Warehouse {result.name} successfully updated!",
                                parent=self.wh_management_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.wh_management_view.parent)
        return result

    def del_warehouse(self):
        selected = self.wh_management_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.wh_management_view.parent)
            return

        wh_id = int(selected[0][0])
        result = self.module.delete_wh_by_id(wh_id)
        if isinstance(result, Warehouse):
            self.reload()
            self.wh_management_view.refresh()
            messagebox.showinfo("Info!", f"Warehouse {result.name} successfully deleted!",
                                parent=self.wh_management_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.wh_management_view.parent)
        return result

    # endregion

    # region Product Management
    def create_product(self, name, type_, b_price, s_price, qty, warehouse):

        result = self.module.create_product_from_view(name, type_, b_price, s_price, qty, warehouse)

        if isinstance(result, Product):
            self.reload()
            self.pr_management_view.refresh()
            messagebox.showinfo("Info!", f"Product {result.name} has been created successfully!",
                                parent=self.pr_management_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.pr_management_view.parent)

        return result

    def update_product(self, name, type_, b_price, s_price, qty, warehouse, id_):
        result = self.module.update_product_from_view(name, type_, b_price, s_price, qty, warehouse, id_)

        if isinstance(result, Product):
            self.reload()
            self.pr_management_view.refresh()
            messagebox.showinfo("Info!", f"Product {result.name} has been updated successfully!",
                                parent=self.pr_management_view.parent)
        else:
            messagebox.showerror("Info!", result, parent=self.pr_management_view.parent)

        return result

    def del_product(self):
        selected = self.pr_management_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.pr_management_view.parent)
            return

        pr_id = int(selected[0][0])
        result = self.module.delete_product_by_id(pr_id)
        if isinstance(result, Product):
            self.reload()
            self.pr_management_view.refresh()
            messagebox.showinfo("Info!", f"Product {result.name} successfully deleted!",
                                parent=self.pr_management_view.parent)
        else:
            messagebox.showerror("Warning", result, parent=self.pr_management_view.parent)

        return result

    # endregion

    # endregion

    # region GUI

    # region Warehouse Management
    def show_create_warehouse(self):
        form = ItemForm(self.wh_management_view.parent, Warehouse("", "", 0, [], ""), self, "Create Warehouse",
                        height=250)

    def show_edit_warehouse(self):
        selected = self.wh_management_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.wh_management_view.parent)
            return

        wh_id = int(selected[0][0])
        warehouse = self.module.find_wh_by_id(wh_id)
        form = ItemForm(self.wh_management_view.parent, warehouse, self, "Update Warehouse", height=250, edit=True)

    # endregion

    # region Product Management
    def show_create_product(self):
        form = ItemForm(self.pr_management_view.parent, Product("", "", 0.0, 0.0, 0, ""), self, "Create Product")

    def show_edit_product(self):
        selected = self.pr_management_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.pr_management_view.parent)
            return

        pr_id = int(selected[0][0])
        product = self.module.find_product_by_id(pr_id)
        form = ItemForm(self.pr_management_view.parent, product, self, "Edit Product", edit=True)

    # endregion

    # endregion

    def close_wh_mgmt(self):
        self.wh_management_view.open_views.remove(self.wh_management_view.page_name)
        self.wh_management_view.parent.destroy()

    def close_product_mgmt(self):
        self.pr_management_view.open_views.remove(self.pr_management_view.page_name)
        self.pr_management_view.parent.destroy()
