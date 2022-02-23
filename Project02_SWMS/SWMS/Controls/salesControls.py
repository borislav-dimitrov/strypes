import Models.Db.fakeDB as DB
from tkinter import *
import Services.tkinterServices as TkServ
from Services.productServices import get_all_sellable_products, get_product_by_id
from Services.clientServices import get_client_by_id
from Services.transactionServices import get_id_for_new_transaction
from Models.Assets.transaction import Transaction
from Services.dateServices import get_time_now
from Models.Data.saveData import save_transactions, save_products


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


def sell(screen, cart, cart_items, sellable_items, selected_client):
    # Check if client is selected
    client = selected_client.get()
    if "none" in client.lower():
        TkServ.create_custom_msg(screen, "Warning!", "You have to chose a client first!")
        return

    try:
        # Get all the objects that we will need for the transaction
        total_price = float(screen.nametowidget("total_price").cget("text"))
        client = get_client_by_id(client.split("|")[0].strip(), DB.clients)
        all_products_in_cart = cart_items.get()
        if len(all_products_in_cart) == 0:
            TkServ.create_custom_msg(screen, "Warning!", "Nothing to sell!")
            return
        all_products_in_cart = cart_items.get()[1:-1:]
        all_products_in_cart = all_products_in_cart.split(", ")
        products_to_delete = []
        products_info_for_transaction = []

        # Store the products as Objects
        for product in all_products_in_cart:
            curr_item_id = product.split("|")[0].strip()[1::]
            curr_product = get_product_by_id(curr_item_id, DB.products)
            products_info_for_transaction.append(curr_product.get_self_info())
            products_to_delete.append(curr_product)

        # Create transaction object
        new_transaction = Transaction(get_id_for_new_transaction(DB.transactions),
                                      "sale",
                                      get_time_now(),
                                      total_price,
                                      client.get_self_info(),
                                      products_info_for_transaction)
        DB.transactions.append(new_transaction)
        save_transactions()

        # Clear cart and total price
        clear_cart(screen, cart, cart_items)

        # Remove the sold products from the db
        # for item in selection:
        #    curr_item_id = item.split("|")[0].strip()[1::]  # This row is old and must be changed
        #    DB.delete_product_by_id(int(curr_item_id))
        #    save_products()

        # Refresh the listbox values after the sale
        sellable_items.set(get_all_sellable_products(DB.products))

        # Set client back to none
        selected_client.set("none")
    except Exception as ex:
        print(ex)
        TkServ.create_custom_msg(screen, "Warning!", ex)


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
