from tkinter import messagebox

from model.entities.product import Product
from model.entities.warehouse import Warehouse
from model.service.logger import MyLogger
from model.service.modules.warehousing_module import WarehousingModule
from view.components.item_form import ItemForm
from view.components.move_product_form import MoveProductForm


class WarehousingController:
    def __init__(self, warehousing_module: WarehousingModule, logger: MyLogger):
        self.module = warehousing_module
        self.logger = logger
        self.wh_management_view = None
        self.pr_management_view = None
        self.warehouses_view = None

    @property
    def warehouses(self):
        return self.module.warehouses

    @property
    def products(self):
        return self.module.products

    @property
    def warehouses_for_dropdown(self):
        return self.module.get_warehouses_data_for_dropdown()

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

    def find_product_by_id(self, id_):
        return self.module.find_product_by_id(id_)

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
            self.logger.log(__file__, f"Created Warehouse - {result.name}.", "INFO")
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
            self.logger.log(__file__, f"Updated Warehouse - {result.name}.", "INFO")
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
            self.logger.log(__file__, f"Deleted Warehouse - {result.name}.", "INFO")
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
            self.logger.log(__file__, f"Created Product - {result.name}.", "INFO")
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
            self.logger.log(__file__, f"Updated Product - {result.name}.", "INFO")
        else:
            messagebox.showerror("Warning!", result, parent=self.pr_management_view.parent)

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
            self.logger.log(__file__, f"Deleted Product - {result.name}.", "INFO")
        else:
            messagebox.showerror("Warning", result, parent=self.pr_management_view.parent)

        return result

    def move_product(self, products: list, move_to):
        if move_to.get() == "None":
            warehouse = None
        else:
            warehouse = self.module.find_wh_by_id(int(move_to.get().split(",")[0][1:].strip()))

        if len(products) == 1:
            result = self.module.product_change_wh(products[0], warehouse)
            if warehouse is None:
                self.logger.log(__file__, f"Moved Product - {products[0].name} to None.", "INFO")
            else:
                self.logger.log(__file__, f"Moved Product - {products[0].name} to {warehouse.name}.", "INFO")
        else:
            results = []
            for product in products:
                result = self.module.product_change_wh(product, warehouse)
                if warehouse is None:
                    self.logger.log(__file__, f"Moved Product - {product.name} to None.", "INFO")
                else:
                    self.logger.log(__file__, f"Moved Product - {product.name} to {warehouse.name}.", "INFO")
            if all(results) == "Ok":
                result = "Ok"

        if result == "Ok":
            messagebox.showinfo("Info!", f"Products moved successfully!",
                                parent=self.warehouses_view.parent)
            self.reload()
            self.warehouses_view.refresh()
        else:
            messagebox.showerror("Error!", result, parent=self.warehouses_view.parent)

        return result

    def cleanup_after_sale(self):
        self.module.cleanup_products_after_sale()
        self.reload()

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

    def filtered_warehouses(self, warehouse: Warehouse):
        return self.module.get_filtered_warehouses(warehouse)

    def refresh_products_treeview_vars(self, view):
        warehouse = view.warehouses_var.get().split(",")[0]
        if warehouse == "None":
            warehouse = None
        else:
            warehouse = int(warehouse[1:])

        products = self.module.find_all_products_in_warehouse(warehouse)
        if isinstance(products, Exception):
            messagebox.showerror("Error!", products, parent=view.parent)
        if products is not None:
            view.treeview_var = products
            view.treeview.set_items(view.treeview_var)
        else:
            view.treeview_var = [Product("None", "None", 0.0, 0.0, 0, None)]
            view.treeview.set_items(view.treeview_var)

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

    def show_move_product(self):
        selected = self.warehouses_view.treeview.get_selected_items()
        selected_wh = self.warehouses_view.warehouses_var.get().split(",")[0]
        if selected_wh == "None":
            selected_wh = None
        else:
            selected_wh = self.module.find_wh_by_id(int(selected_wh[1:]))

        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.warehouses_view.parent)
            return
        elif len(selected) == 1:
            MoveProductForm(self.warehouses_view.parent, self,
                            [self.module.find_product_by_id(int(selected[0][0]))], selected_wh)
        elif len(selected) > 1:
            products = []
            for item in selected:
                products.append(self.module.find_product_by_id(int(item[0])))

            MoveProductForm(self.warehouses_view.parent, self, products, selected_wh)

    # endregion

    # endregion

    def close_wh_mgmt(self):
        self.wh_management_view.open_views.remove(self.wh_management_view.page_name)
        self.wh_management_view.parent.destroy()

    def close_product_mgmt(self):
        self.pr_management_view.open_views.remove(self.pr_management_view.page_name)
        self.pr_management_view.parent.destroy()

    def close_warehouses(self):
        self.warehouses_view.open_views.remove(self.warehouses_view.page_name)
        self.warehouses_view.parent.destroy()
