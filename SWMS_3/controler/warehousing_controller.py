from tkinter import messagebox

from model.entities.warehouse import Warehouse
from model.service.logger import MyLogger
from model.service.modules.warehousing_module import WarehousingModule
from view.components.item_form import ItemForm


class WarehousingController:
    def __init__(self, warehousing_module: WarehousingModule, logger: MyLogger):
        self.module = warehousing_module
        self.logger = logger
        self.management_view = None
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
    def create_warehouse(self, name, type_, capacity, products, status):
        result = self.module.create_wh(name, type_, capacity, [], status)
        if isinstance(result, Warehouse):
            self.reload()
            self.management_view.refresh()
        return result

    def update_warehouse(self, name, type_, capacity, products, status, id_):
        old = self.module.find_wh_by_id(id_)
        result = self.module.update_warehouse(old, name, type_, capacity, products, status)
        if isinstance(result, Warehouse):
            self.reload()
            self.management_view.refresh()
        return result

    def del_warehouse(self):
        selected = self.management_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showwarning("Warning!", "Please make a selection first!", parent=self.management_view.parent)
            return

        wh_id = int(selected[0][0])
        result = self.module.delete_wh_by_id(wh_id)
        if isinstance(result, Warehouse):
            self.reload()
            self.management_view.refresh()
            messagebox.showinfo("Info!", f"Warehouse {result.name} successfully deleted!",
                                parent=self.management_view.parent)
        else:
            messagebox.showwarning("Warning", result, parent=self.management_view.parent)

    # endregion

    # region GUI
    def show_create_warehouse(self):
        form = ItemForm(self.management_view.parent, Warehouse("", "", 0, [], ""), self, height=250)

    def show_edit_warehouse(self):
        selected = self.management_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showwarning("Warning!", "Please make a selection first!", parent=self.management_view.parent)
            return

        wh_id = int(selected[0][0])
        warehouse = self.module.find_wh_by_id(wh_id)
        form = ItemForm(self.management_view.parent, warehouse, self, height=250, edit=True)

    # endregion

    def close(self):
        self.management_view.open_views.remove(self.management_view.page_name)
        self.management_view.parent.destroy()
