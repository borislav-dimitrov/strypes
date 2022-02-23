import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
from Services.suppliersServices import validate_supp_menu
from tkinter import *


def get_data_for_available_products(screen, selected_supplier):
    info = []
    for supplier in DB.suppliers:
        is_valid, status, items = validate_supp_menu(supplier.buy_menu)
        if is_valid and len(items) == 3 and supplier.supp_name == selected_supplier.supplier_name:
            info.append(f"{items[0]}-{items[1]}-{items[2]}")
        else:
            TkServ.create_custom_msg(screen, "Warning!", f"Something is wrong in {supplier.supp_name} menu data!")
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
        if item != "":
            if item[0] == " ":
                curr_price = item[1:-1:].split("|")[2].strip()
            else:
                curr_price = item.split("|")[2].strip()[:-1:]
            total += float(curr_price)

    total_lbl.config(text=total)


def on_supplier_change(screen):
    listbox = screen.nametowidget("available_lb_frame").nametowidget("available_lb")

    data = get_data_for_available_products(screen)
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
    available_lb.delete(selection_index)
    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def rem_item_from_cart(screen, cart_lb, available_lb, cart_items):
    pass


def clear_cart(screen, cart_lb, cart_items):
    pass


def buy(screen, cart_lb, cart_items, sellable_items, selected_client_var):
    pass
