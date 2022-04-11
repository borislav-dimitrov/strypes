from tkinter import messagebox

import view.utils.tkinter_utils as tkutil
from controler.warehousing_controller import WarehousingController
from model.entities.counterparty import Counterparty
from model.entities.invoices import Invoice
from model.entities.product import Product
from model.entities.transaction import Transaction
from model.service.logger import MyLogger
from model.service.modules.sales_module import SalesModule
from view.components.item_form import ItemForm


class SalesController:
    def __init__(self, sales_module: SalesModule, wh_module: WarehousingController, logger: MyLogger):
        self.module = sales_module
        self.wh_controller = wh_module
        self.logger = logger
        self.counterparty_view = None
        self.sales_view = None
        self.pur_view = None
        self.tr_view = None

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

    # region FIND

    def gen_clients_for_treeview(self):
        return self.module.find_all_clients_for_dropdown()

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

    def generate_treeview_for_wh_products(self, view):
        return self.wh_controller.generate_treeview_for_wh_products(view)

    def warehouses_for_dropdown(self):
        return self.wh_controller.warehouses_for_dropdown

    def find_all_products_in_warehouse(self, id_: int | None):
        return self.wh_controller.module.find_all_products_in_warehouse(id_)

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

    # region SALES

    def sell_add_item_to_cart(self):
        selection = self.sales_view.treeview.get_selected_items()
        if len(selection) == 0:
            messagebox.showerror("Error!", "First make a selection!", parent=self.sales_view.parent)
            return

        selected_product = self.wh_controller.module.find_product_by_id(int(selection[0][0]))
        amount = self.sales_view.amount_entry.get()
        if not amount.isnumeric() or int(amount) <= 0:
            messagebox.showerror("Error!", "Amount must be positive Number", parent=self.sales_view.parent)
            return
        result, product = self.module.sale_reduce_quantity_or_sell_all(selected_product, int(amount))

        if result != "Not enough to sell!":
            self.module.sell_add_item_to_cart(self.sales_view.shopping_cart_var, product)
        else:
            messagebox.showerror("Error!", result, parent=self.sales_view.parent)
            return
        self.sales_view.total_price_var.set(f"Total Price: "
                                            f"{self.module.sell_calc_total_price(self.sales_view.shopping_cart_var)} BGN")
        self.sales_view.refresh()

    def sell_rem_item_from_cart(self):
        selection = self.sales_view.shopping_cart.get_selected_items()
        if len(selection) == 0:
            messagebox.showerror("Error!", "First make a selection!", parent=self.sales_view.parent)
            return

        self.module.sale_rem_item_from_cart(self.wh_controller.find_product_by_id,
                                            self.sales_view.shopping_cart_var, selection[0])

        self.sales_view.total_price_var.set(f"Total Price: "
                                            f"{self.module.sell_calc_total_price(self.sales_view.shopping_cart_var)} BGN")
        self.sales_view.refresh()

    def sell_clear_cart(self):
        self.module.sell_clear_cart(self.wh_controller.find_product_by_id, self.sales_view.shopping_cart_var)
        self.sales_view.total_price_var.set(f"Total Price: "
                                            f"{self.module.sell_calc_total_price(self.sales_view.shopping_cart_var)} BGN")
        self.sales_view.refresh()

    def sell(self):
        result = self.module.make_a_sale(self.sales_view.shopping_cart_var, self.sales_view.clients_var.get())
        if isinstance(result, Transaction):
            messagebox.showinfo("Info!", "Transaction successful!", parent=self.sales_view.parent)
            self.sales_view.shopping_cart_var.clear()
            self.wh_controller.cleanup_after_sale()
            self.reload()
            self.sales_view.total_price_var.set(f"Total Price: "
                                                f"{self.module.sell_calc_total_price(self.sales_view.shopping_cart_var)} BGN")
            self.sales_view.refresh()
        else:
            messagebox.showerror("Error!", result, parent=self.sales_view.parent)

    # endregion

    # region PURCHASES

    def pur_add_to_cart(self):
        selection = self.pur_view.treeview.get_selected_items()
        if len(selection) == 0:
            messagebox.showerror("Error!", "First make a selection!", parent=self.pur_view.parent)
            return

        amount = self.pur_view.amount_entry.get()
        if not amount.isnumeric() or int(amount) <= 0:
            messagebox.showerror("Error!", "Amount must be positive Number", parent=self.pur_view.parent)
            return

        selection = self.pur_view.treeview.get_selected_items()[0][1:]
        selected_product = Product(selection[0], selection[1], float(selection[2]),
                                   float(selection[3]), int(amount), None)

        self.module.pur_add_item_to_cart(self.pur_view.shopping_cart_var, selected_product)

        self.pur_view.total_price_var.set(f"Total Price: "
                                          f"{self.module.sell_calc_total_price(self.pur_view.shopping_cart_var)} BGN")
        self.pur_view.refresh()

    def pur_rem_from_cart(self):
        selection = self.pur_view.shopping_cart.get_selected_items()[0]
        if len(selection) == 0:
            messagebox.showerror("Error!", "First make a selection!", parent=self.pur_view.parent)
            return

        self.module.pur_rem_item_from_cart(self.pur_view.shopping_cart_var, selection)

        self.pur_view.total_price_var.set(f"Total Price: "
                                          f"{self.module.sell_calc_total_price(self.pur_view.shopping_cart_var)} BGN")
        self.pur_view.refresh()

    def pur_clear_cart(self):
        self.pur_view.shopping_cart_var.clear()
        self.pur_view.total_price_var.set(f"Total Price: "
                                          f"{self.module.sell_calc_total_price(self.pur_view.shopping_cart_var)} BGN")
        self.pur_view.refresh()

    def buy(self):
        cart_items = self.pur_view.shopping_cart_var
        supplier = self.module.find_counterparty_by_id(int(self.pur_view.suppliers_var.get().split(", ")[0][1:]))
        tr_items = []
        for item in cart_items:
            result = self.wh_controller.module.create_product(item.name, item.type, item.buy_price, item.sell_price,
                                                              item.quantity, None)
            if isinstance(result, Exception):
                messagebox.showerror("Error!")
            else:
                tr_items.append(result)

        tr = self.module.create_tr("Purchase", supplier, tr_items)
        if isinstance(tr, Transaction):
            messagebox.showinfo("Info!", "Transaction successful!", parent=self.pur_view.parent)
            self.pur_view.shopping_cart_var.clear()
            self.wh_controller.cleanup_after_sale()
            self.reload()
            self.pur_view.total_price_var.set(f"Total Price: "
                                              f"{self.module.sell_calc_total_price(self.pur_view.shopping_cart_var)} BGN")
            self.pur_view.refresh()
        else:
            messagebox.showerror("Error!", "Transaction Failed!", parent=self.pur_view.parent)

    def suppliers_for_dropdown(self):
        return self.module.get_suppliers_for_dropdown()

    def get_supplier_products(self, supplier_id: int | None = None):
        return self.module.get_supplier_products(supplier_id)

    def on_suppl_change(self):
        selected_supplier_id = int(self.pur_view.suppliers_var.get().split(", ")[0][1:])
        self.pur_view.treeview_var = self.get_supplier_products(selected_supplier_id)
        self.pur_view.shopping_cart_var.clear()
        self.pur_view.total_price_var.set(f"Total Price: "
                                          f"{self.module.sell_calc_total_price(self.pur_view.shopping_cart_var)} BGN")
        self.pur_view.refresh()

    # endregion

    # region INVOICES
    def gen_invoice(self):
        selection = self.tr_view.item_list.get_selected_items()
        if len(selection) == 0:
            messagebox.showerror("Error!", "Make a selection first!", parent=self.tr_view.parent)
            return
        transaction = self.module.find_transaction_by_id(int(selection[0][0]))
        inv = self.module.gen_inv_from_tr(transaction)
        if isinstance(inv, Invoice):
            messagebox.showinfo("Info!", f"Invoice #{inv.number} generated successfully!", parent=self.tr_view.parent)
            self.preview_invoice()
            self.reload()
            self.tr_view.refresh()
        else:
            messagebox.showerror("Error!", inv, parent=self.tr_view.parent)

    def del_invoice(self):
        selection = self.tr_view.item_list.get_selected_items()
        if len(selection) == 0:
            messagebox.showerror("Error!", "Make a selection first!", parent=self.tr_view.parent)
            return
        transaction = self.module.find_transaction_by_id(int(selection[0][0]))
        result = self.module.del_inv_by_transaction(transaction)
        if isinstance(result, Invoice):
            messagebox.showinfo("Info!", f"Invoice #{result.number} deleted successfully!", parent=self.tr_view.parent)
            self.reload()
            self.tr_view.refresh()
        else:
            messagebox.showerror("Error!", result, parent=self.tr_view.parent)

    def preview_invoice(self):
        selection = self.tr_view.item_list.get_selected_items()
        if len(selection) == 0:
            messagebox.showerror("Error!", "Make a selection first!", parent=self.tr_view.parent)
            return
        transaction = self.module.find_transaction_by_id(int(selection[0][0]))
        invoice = transaction.invoice
        if invoice is None:
            messagebox.showerror("Error!", "This transaction has no Invoice!", parent=self.tr_view.parent)
            return

        state, msg = self.module.generate_invoice_pdf(invoice)
        if not state:
            messagebox.showerror("Error!", msg, parent=self.tr_view.parent)

    # endregion

    # endregion

    def close_counterparty(self):
        self.counterparty_view.open_views.remove(self.counterparty_view.page_name)
        self.counterparty_view.parent.destroy()

    def close_sales(self):
        self.module.rollback_unfinished_sales(self.wh_controller.find_product_by_id, self.sales_view.shopping_cart_var)
        self.sales_view.open_views.remove(self.sales_view.page_name)
        self.sales_view.parent.destroy()

    def close_pur(self):
        self.pur_view.open_views.remove(self.pur_view.page_name)
        self.pur_view.parent.destroy()

    def close_tr(self):
        self.tr_view.open_views.remove(self.tr_view.page_name)
        self.tr_view.parent.destroy()
