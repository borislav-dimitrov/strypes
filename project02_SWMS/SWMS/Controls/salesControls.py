import Models.Db.fakeDB as DB
import tkinter as tk
import Services.tkinterServices as TkServ
import Services.productServices as ProdServ
import Services.warehouseServices as WhServ
from Services.clientServices import get_client_by_id
from Services.transactionServices import get_id_for_new_transaction
from Models.Assets.transaction import Transaction
from Services.dateServices import get_time_now


def destruct_sellable_item(item_info):
    split = item_info.split("|")
    info = {
        "product_id": split[0].strip(),
        "product_name": split[1].strip(),
        "warehouse": split[2].strip(),
        "sell_price": split[3].strip(),
        "quantity": split[4].strip(),
    }
    return info


def check_product_in_cart(items, match_item):
    selection = items.get()
    if len(selection) <= 0:
        return False, -1
    items_in_cart = []
    items_in_cart_without_quantity = []
    selection = selection[1:-1:]
    selection = selection.split(",")
    for item in selection:
        if item != "":
            if item[0] == " ":
                items_in_cart.append(item[2:-1:])
                items_in_cart_without_quantity.append(
                    f"{item[2:-1:].split('|')[0].strip()} | {item[1:-1:].split('|')[1].strip()} | "
                    f"{item[1:-1:].split('|')[2].strip()} | {item[1:-1:].split('|')[3].strip()}")
            else:
                items_in_cart.append(item[1:-1:])
                items_in_cart_without_quantity.append(
                    f"{item[1::].split('|')[0].strip()} | {item.split('|')[1].strip()} | "
                    f"{item.split('|')[2].strip()} | {item[1:-1:].split('|')[3].strip()}")

    for item in range(len(items_in_cart_without_quantity)):
        if match_item.strip() in items_in_cart_without_quantity[item]:
            return True, items_in_cart[item]
    return False, -1


def calc_and_set_total_price(screen, items):
    total_lbl = screen.nametowidget("total_price")
    total = 0.00

    # Format the data
    selection = items.get()
    if len(selection) == 0:
        TkServ.create_custom_msg(screen, "Warning!", "Nothing to sell!")
        return

    selection = selection[1:-1:]
    selection = selection.split(",")
    for item in selection:
        if item != "":
            if item[0] == " ":
                curr_price = item[::].split("|")[3].strip()
                quantity = item[1:-1:].split("|")[4].strip()
                total += float(curr_price) * float(quantity)
            else:
                curr_price = item.split("|")[3].strip()
                quantity = item.split("|")[4].strip()[:-1:]
                total += float(curr_price) * float(quantity)

    total_lbl.config(text=total)


def sell(screen, cart, cart_items, sellable_lb, sellable_items, selected_client):
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
            curr_prod_id = product.split("|")[0].strip()[1::]
            if product[len(product) - 1] == "'":
                curr_prod_sold_quantity = product.split("|")[4].strip()[:-1:]
            else:
                curr_prod_sold_quantity = product.split("|")[4].strip()[:-2:]

            curr_product = ProdServ.get_product_by_id(curr_prod_id, DB.products)
            assigned_wh = WhServ.get_wh_by_name(curr_product.assigned_to_wh, DB.warehouses)

            # Reduce quantity from product and warehouse
            WhServ.remove_product(assigned_wh, curr_product.product_id, curr_prod_sold_quantity)
            curr_product.quantity -= int(curr_prod_sold_quantity)

            products_info_for_transaction.append(f"ID: {curr_product.product_id} | "
                                                 f"Name: {curr_product.product_name} | "
                                                 f"Type: {curr_product.product_type} | "
                                                 f"Sell Price: {curr_product.sell_price} | "
                                                 f"Assigned to: {curr_product.assigned_to_wh} | "
                                                 f"Amount sold: {curr_prod_sold_quantity}")

            if curr_product.quantity <= 0:
                products_to_delete.append(curr_product)

        if len(products_to_delete) > 0:
            for i in range(len(products_to_delete)):
                DB.products.remove(products_to_delete[i])

        # Create transaction object
        new_transaction = Transaction(get_id_for_new_transaction(DB.transactions),
                                      "sale",
                                      get_time_now(),
                                      total_price,
                                      client.get_self_info(),
                                      products_info_for_transaction)
        DB.transactions.append(new_transaction)

        DB.save_all_data()
        DB.load_all_entities()
        DB.my_logger.log(__file__, f"{DB.curr_user} made a sale with id: {new_transaction.tr_id}", "INFO")

        # Clear cart and total price and repopulate sellable items
        clear_cart(screen, cart, cart_items, sellable_lb)

        # Set client back to none
        selected_client.set("none")
    except Exception as ex:
        print(ex)
        TkServ.create_custom_msg(screen, "Warning!", ex)


def add_item_to_cart(screen, cart, cart_items, sellable, sellable_items, multiplier):
    if len(sellable.curselection()) == 0:
        TkServ.create_custom_msg(screen, "Warning!", "Nothing selected!")
        return
    if int(multiplier) <= 0:
        TkServ.create_custom_msg(screen, "Warning!", "Multiplier must be positive!")
        return

    # Get current selection
    selection_index = sellable.curselection()[0]
    current_selection = sellable.get(selection_index)
    item_info = destruct_sellable_item(current_selection)

    # Check if there are enough products to sell
    if int(multiplier) > int(item_info["quantity"]):
        TkServ.create_custom_msg(screen, "Warning!", "Not enough products! Reduce the multiplier!")
        return

    new_info = f"{item_info['product_id']} | {item_info['product_name']} | " \
               f"{item_info['warehouse']} | {item_info['sell_price']}"
    new_quantity = int(item_info['quantity']) - int(multiplier)

    # Change sellable products
    if new_quantity > 0:
        TkServ.modify_listbox_value(sellable, sellable_items, current_selection, f"{new_info} | {new_quantity}")
    else:
        sellable.delete(selection_index)

    # Add products to cart
    already_exist, item_in_cart = check_product_in_cart(cart_items, new_info)
    if not already_exist:
        cart.insert(tk.END, f"{new_info} | {multiplier}")
    else:
        modify_cart_item = item_in_cart.split("|")[len(item_in_cart.split("|")) - 1].strip()
        modify_cart_item = f"{new_info} | {int(modify_cart_item) + int(multiplier)}"
        TkServ.modify_listbox_value(cart, cart_items, item_in_cart, modify_cart_item)

    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def rem_item_from_cart(screen, cart, cart_items, sellable, sellable_items, multiplier):
    # If nothing selected - return
    if len(cart.curselection()) == 0:
        return
    if int(multiplier) <= 0:
        TkServ.create_custom_msg(screen, "Warning!", "Multiplier must be positive!")
        return

    # Get current selection
    selection_index = cart.curselection()[0]
    current_selection = cart.get(selection_index)
    item_info = destruct_sellable_item(current_selection)

    # Check if there are enough products to remove
    if int(multiplier) > int(item_info["quantity"]):
        TkServ.create_custom_msg(screen, "Warning!", "Not enough products! Reduce the multiplier!")
        return

    new_info = f"{item_info['product_id']} | {item_info['product_name']} | " \
               f"{item_info['warehouse']} | {item_info['sell_price']}"
    new_quantity = int(item_info['quantity']) - int(multiplier)

    # Change cart products
    if new_quantity > 0:
        TkServ.modify_listbox_value(cart, cart_items, current_selection, f"{new_info} | {new_quantity}")
    else:
        cart.delete(selection_index)

    # return products to sellable listbox
    already_exist, item_in_sellable = check_product_in_cart(sellable_items, new_info)
    if not already_exist:
        sellable.insert(tk.END, f"{new_info} | {multiplier}")
    else:
        modify_sellable_item = item_in_sellable.split("|")[len(item_in_sellable.split("|")) - 1].strip()
        modify_sellable_item = f"{new_info} | {int(modify_sellable_item) + int(multiplier)}"
        TkServ.modify_listbox_value(sellable, sellable_items, item_in_sellable, modify_sellable_item)

    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def clear_cart(screen, cart, cart_items, sellable_lb):
    cart.delete(0, tk.END)

    # Calculate total price
    calc_and_set_total_price(screen, cart_items)

    # Repopulate sellable products
    sellable_lb.delete(0, tk.END)
    sellable_products = ProdServ.get_all_sellable_products(DB.products)
    for product in sellable_products:
        sellable_lb.insert(tk.END, product)


def on_client_change():
    pass
