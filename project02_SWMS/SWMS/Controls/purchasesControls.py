import Models.Db.fakeDB as DB
import Models.Data.saveData as Save
import Services.tkinterServices as TkServ
import Services.suppliersServices as SuppServ
import Services.productServices as ProdServ
import Services.transactionServices as TransServ
import Services.dateServices as DateServ
from Models.Assets.transaction import Transaction
import tkinter as tk


def destruct_purchaseable_item(item_info, separator="-", get_amount=False):
    split = item_info.split(separator)
    info = {
        "product_name": split[0].strip(),
        "product_type": split[1].strip(),
        "buy_price": split[2].strip(),      
    }
    if get_amount:
        info["amount"] = split[3].strip()

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


def get_data_for_available_products(screen, selected_supplier):
    info = []
    for supplier in DB.suppliers:
        if supplier.supp_name == selected_supplier.supp_name:
            is_valid, status, items = SuppServ.validate_supp_menu(supplier.buy_menu)

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
            curr_price = item[2:-1:].split("|")[2].strip()
            quantity = item[1:-1:].split("|")[3].strip()
            total += float(curr_price) * float(quantity)
        elif item != "":
            curr_price = item[1:-1:].split("|")[2].strip()
            quantity = item.split("|")[3].strip()[:-1:]
            total += float(curr_price) * float(quantity)

    total_lbl.config(text=total)


def on_supplier_change(screen, selected_supplier):
    listbox = screen.nametowidget("available_lb_frame").nametowidget("available_lb")
    supplier_id = selected_supplier.get().split("|")[0].strip()
    supplier = SuppServ.get_supplier_by_id(supplier_id, DB.suppliers)
    data = get_data_for_available_products(screen, supplier)
    # Change total price

    # Clear listbox
    listbox.delete(0, tk.END)

    # Insert the new data
    for item in data:
        listbox.insert(tk.END, item)


def add_item_to_cart(screen, cart_lb, available_lb, cart_items, multiplier):
    if len(available_lb.curselection()) == 0:
        return
    if int(multiplier) <= 0:
        TkServ.create_custom_msg(screen, "Warning!", "Multiplier must be positive!")
        return

    selection_index = available_lb.curselection()[0]
    current_selection = available_lb.get(selection_index)
    item_info = destruct_purchaseable_item(current_selection)

    new_info = f"{item_info['product_name']} | {item_info['product_type']} | " \
               f"{item_info['buy_price']}"

    already_exist, item_in_cart = check_product_in_cart(cart_items, new_info)
    
    if not already_exist:
        cart_lb.insert(tk.END, f"{new_info} | {multiplier}")
    else:
        modify_cart_item = item_in_cart.split("|")[len(item_in_cart.split("|")) - 1].strip()
        modify_cart_item = f"{new_info} | {int(modify_cart_item) + int(multiplier)}"
        TkServ.modify_listbox_value(cart_lb, cart_items, item_in_cart, modify_cart_item)
    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def rem_item_from_cart(screen, cart_lb, cart_items, multiplier):
    # If nothing selected - return
    if len(cart_lb.curselection()) == 0:
        return
    if int(multiplier) <= 0:
        TkServ.create_custom_msg(screen, "Warning!", "Multiplier must be positive!")
        return
    # Get current selection
    selection_index = cart_lb.curselection()[0]
    current_selection = cart_lb.get(selection_index)
    item_info = destruct_purchaseable_item(current_selection, separator="|", get_amount=True)

    # Check if there are enough products to remove
    if int(multiplier) > int(item_info["amount"]):
        TkServ.create_custom_msg(screen, "Warning!", "Not enough products! Reduce the multiplier!")
        return

    new_info = f"{item_info['product_name']} | {item_info['product_type']} | " \
               f"{item_info['buy_price']}"
    new_quantity = int(item_info['amount']) - int(multiplier)

    # Change cart products
    if new_quantity > 0:
        TkServ.modify_listbox_value(cart_lb, cart_items, current_selection, f"{new_info} | {new_quantity}")
    else:
        cart_lb.delete(selection_index)

    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def clear_cart(screen, cart_lb, cart_items):
    cart_lb.delete(0, tk.END)

    # Calculate total price
    calc_and_set_total_price(screen, cart_items)


def buy(screen, cart_lb, cart_items, sellable_items, selected_supplier_var):
    supplier = selected_supplier_var.get()
    try:
        # Get all the objects that we will need for the transaction
        total_price = float(screen.nametowidget("total_price").cget("text"))
        supplier = SuppServ.get_supplier_by_id(supplier.split("|")[0].strip(), DB.suppliers)
        all_products_in_cart = cart_items.get()

        if len(all_products_in_cart) == 0:
            TkServ.create_custom_msg(screen, "Warning!", "Nothing to sell!")
            return

        all_products_in_cart = all_products_in_cart[1:-1:]
        all_products_in_cart = all_products_in_cart.split(", ")

        # Store the data for the new products
        new_products_info = []
        newly_created_products_id = []
        if len(all_products_in_cart) == 1:
            for product in all_products_in_cart:
                curr_item_id = ProdServ.get_id_for_new_product(DB.products)
                curr_item_name = product.split("|")[0].strip()[1::]
                curr_item_type = product.split("|")[1].strip()
                curr_item_price = float(product.split("|")[2].strip())
                curr_item_amount = float(product.split("|")[3].strip()[:-2:])

                new_product = {
                    "product_name": curr_item_name,
                    "product_type": curr_item_type,
                    "buy_price": curr_item_price,
                    "sell_price": curr_item_price + (curr_item_price * 0.20),
                    "assigned_to_wh": "none",
                    "quantity": int(curr_item_amount)
                }
                new_products_info.append(new_product)
                newly_created_products_id.append(curr_item_id)
        else:
            for product in all_products_in_cart:
                curr_item_id = ProdServ.get_id_for_new_product(DB.products)
                curr_item_name = product.split("|")[0].strip()[1::]
                curr_item_type = product.split("|")[1].strip()
                curr_item_price = float(product.split("|")[2].strip())
                curr_item_amount = float(product.split("|")[3].strip()[:-1:])

                new_product = {
                    "product_name": curr_item_name,
                    "product_type": curr_item_type,
                    "buy_price": curr_item_price,
                    "sell_price": curr_item_price + (curr_item_price * 0.20),
                    "assigned_to_wh": "none",
                    "quantity": int(curr_item_amount)
                }
                new_products_info.append(new_product)
                newly_created_products_id.append(curr_item_id)

        # Create new products
        DB.create_products(new_products_info)
        DB.save_products()

        # Create transaction object
        new_transaction = Transaction(TransServ.get_id_for_new_transaction(DB.transactions), "purchase", DateServ.get_time_now(), total_price,
                                      supplier.get_self_info(),
                                      ProdServ.get_products_info_by_id(newly_created_products_id, DB.products))
        DB.transactions.append(new_transaction)
        Save.save_transactions()

        # Clear cart and total price
        clear_cart(screen, cart_lb, cart_items)

    except Exception as ex:
        print(ex)
        TkServ.create_custom_msg(screen, "Warning!", ex)
