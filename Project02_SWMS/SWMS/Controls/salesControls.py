import Models.Db.fakeDB as DB
from tkinter import *
import Services.tkinterServices as TkServ
from Services.productServices import get_all_sellable_products


def calc_and_set_total_price(screen, items):
    total_lbl = screen.nametowidget("total_price")
    #chosen_client = screen.sel_client.get()

    total = 0.00

    #print(chosen_client)

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


def sell(screen, cart, cart_items, sellable_items):
    # Clear cart and total price
    clear_cart(screen, cart, cart_items)

    # Remove the sold products from the db
    # for item in selection:
    #    curr_item_id = item.split("|")[0].strip()[1::]
    #    DB.delete_product_by_id(int(curr_item_id))

    # Refresh the listbox values after the sale
    sellable_items.set(get_all_sellable_products(DB.products))

    # Create transaction object


def add_item_to_cart(screen, cart, sellable, cart_items):
    selection_index = sellable.curselection()[0]
    current_selection = sellable.get(selection_index)

    cart.insert(END, current_selection)
    sellable.delete(selection_index)
    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def rem_item_from_cart(screen, cart, sellable, cart_items):
    # If nothing selected - return
    if len(cart.curselection()) == 0:
        return
    selection_index = cart.curselection()[0]
    current_selection = cart.get(selection_index)

    sellable.insert(END, current_selection)
    cart.delete(selection_index)

    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def clear_cart(screen, cart, items):
    # Calculate total price
    calc_and_set_total_price(screen, items)

    cart.delete(0, END)


def on_client_change():
    pass