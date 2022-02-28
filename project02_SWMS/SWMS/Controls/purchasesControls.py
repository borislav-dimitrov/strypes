import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
from Services.suppliersServices import validate_supp_menu, get_supplier_by_id
from tkinter import *


def get_data_for_available_products(screen, selected_supplier):
    info = []
    for supplier in DB.suppliers:
        if supplier.supp_name == selected_supplier.supp_name:
            is_valid, status, items = validate_supp_menu(supplier.buy_menu)

            if not is_valid:
                TkServ.create_custom_msg(screen, "Warning!", f"Something is wrong in {supplier.supp_name} menu data!")
                return

            # If 1 item
            if len(items) == 1:
                info.append(items[0])
            # If more than 1 item
            else:
                for item in items:
                    info.append(item)
    if len(info) == 0:
        TkServ.create_custom_msg(screen, "Warning!", f"Something is wrong in {selected_supplier.supp_name} menu data!")
        return
    return info


def calc_and_set_total_price(screen, items):
    total_lbl = screen.nametowidget("total_price")
    total = 0.00

    # Format the data
    selection = items.get()
    if len(selection) == 0:  # and check for selected client
        TkServ.create_custom_msg(screen, "Warning!", "Nothing to sell!")
        return

    selection = selection[1:-1:]
    selection = selection.split(",")
    for item in selection:
        if item != "" and item[0] == " ":
            item_name = item[2:-1:].split("-")[0].strip()
            item_type = item[2:-1:].split("-")[1].strip()
            item_price = item[2:-1:].split("-")[2].strip()
            total += float(item_price)
        elif item != "":
            item_name = item[1:-1:].split("-")[0].strip()
            item_type = item[1:-1:].split("-")[1].strip()
            item_price = item[1:-1:].split("-")[2].strip()
            total += float(item_price)

    total_lbl.config(text=total)


def on_supplier_change(screen, selected_supplier):
    listbox = screen.nametowidget("available_lb_frame").nametowidget("available_lb")
    supplier_id = selected_supplier.get().split("|")[0].strip()
    supplier = get_supplier_by_id(supplier_id, DB.suppliers)
    data = get_data_for_available_products(screen, supplier)
    # Change total price

    # Clear listbox
    listbox.delete(0, END)

    # Insert the new data
    for item in data:
        listbox.insert(END, item)


def add_item_to_cart(screen, cart_lb, available_lb, cart_items):
    selection_index = available_lb.curselection()[0]
    current_selection = available_lb.get(selection_index)

    cart_lb.insert(END, current_selection)
    # available_lb.delete(selection_index)
    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def rem_item_from_cart(screen, cart_lb, available_lb, cart_items):
    pass


def clear_cart(screen, cart_lb, cart_items):
    pass


def buy(screen, cart_lb, cart_items, sellable_items, selected_client_var):
    pass
