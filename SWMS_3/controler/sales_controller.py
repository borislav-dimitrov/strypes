from tkinter import messagebox

from model.entities.counterparty import Counterparty
from model.service.logger import MyLogger
from model.service.modules.sales_module import SalesModule
from view.components.item_form import ItemForm


class SalesController:
    def __init__(self, sales_module: SalesModule, logger: MyLogger):
        self.module = sales_module
        self.logger = logger
        self.counterparty_view = None

    @property
    def counterparties(self):
        return self.module.counterparties

    @property
    def transactions(self):
        return self.module.transactions

    @property
    def invoices(self):
        return self.module.invoices

    # region Save/Load/Reload

    def load_all(self):
        self.module.load_all()

    def save_all(self):
        self.module.save_all()

    def reload(self):
        self.save_all()
        self.load_all()

    # endregion

    # region CRUD
    def create_counterparty(self, name, phone, payment_nr, status, type_, description):
        result = self.module.create_cpty_from_view(name, phone, payment_nr, status, type_, description)

        if isinstance(result, Counterparty):
            self.reload()
            self.counterparty_view.refresh()
            messagebox.showinfo("Info!", f"Counterparty {result.name} created successfully!",
                                parent=self.counterparty_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.counterparty_view.parent)

        return result

    def update_counterparty(self, name, phone, payment_nr, status, type_, description, id_):
        result = self.module.update_cpty_from_view(name, phone, payment_nr, status, type_, description, id_)

        if isinstance(result, Counterparty):
            self.reload()
            self.counterparty_view.refresh()
            messagebox.showinfo("Info!", f"Counterparty {result.name} updated successfully!",
                                parent=self.counterparty_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.counterparty_view.parent)
        return result

    def del_counterparty(self):
        warning_msg = """
        This will delete the counterparty with all of his transactions/invoices.
        If you want to soft delete, change status to Disabled and the counterparty won't be visible"""
        warning_msg += " in the Operators interface, while history for transactions/invoices will still be accessible."

        selected = self.counterparty_view.item_list.get_selected_items()

        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.counterparty_view.parent)
            return
        answer = messagebox.askyesno(title="Are you sure?", message=warning_msg, parent=self.counterparty_view.parent)
        if not answer:
            return

        cpty_id = int(selected[0][0])
        result = self.module.del_cpty_from_view(cpty_id)

        if isinstance(result, Counterparty):
            self.reload()
            self.counterparty_view.refresh()
            messagebox.showinfo("Info!", f"Counterparty {result.name} successfully deleted!",
                                parent=self.counterparty_view.parent)
        else:
            messagebox.showerror("Error!", result, parent=self.counterparty_view.parent)

    # endregion

    # region VIEW
    def show_create_counterparty(self):
        form = ItemForm(self.counterparty_view.parent,
                        Counterparty("", "", "", "", "", ""), self, "Create Counterparty", height=250)

    def show_update_counterparty(self):
        selected = self.counterparty_view.item_list.get_selected_items()
        if len(selected) < 1:
            messagebox.showerror("Warning!", "Please make a selection first!", parent=self.counterparty_view.parent)
            return

        counterparty_id = int(selected[0][0])
        counterparty = self.module.find_counterparty_by_id(counterparty_id)

        form = ItemForm(self.counterparty_view.parent, counterparty, self, "Update Counterparty", height=250, edit=True)

    # endregion

    def close_counterparty(self):
        self.counterparty_view.open_views.remove(self.counterparty_view.page_name)
        self.counterparty_view.parent.destroy()
