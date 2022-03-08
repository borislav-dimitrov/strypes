import tkinter.messagebox
from tkinter import *
import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
import Services.productServices as ProdServ
import Services.warehouseServices as WhServ
from Models.Data.saveData import save_products


def clear_prod_screen(screen):
    clear_all_but = ["edit_prod_btn", "new_prod_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="Create/Modify Products")


def clear_product_properties(screen):
    clear_all_but = ["edit_prod_btn", "new_prod_btn", "header_lbl", "!optionmenu"]
    for widget in screen.grid_slaves():
        current = str(widget).split(".").pop()
        if current not in clear_all_but:
            widget.destroy()
        if current == "!optionmenu2":
            widget.destroy()


def delete_product(screen, sel_prod):
    result = tkinter.messagebox.askquestion("Question...",
                                            f"Are you sure you want\nto delete the product\n{sel_prod.product_name}",
                                            parent=screen)
    if result == "yes":
        u_index = ProdServ.get_prod_index_by_id(sel_prod.product_id, DB.products)
        if u_index:
            try:
                DB.products.pop(u_index)
                save_products()
                clear_prod_screen(screen)
                TkServ.create_custom_msg(screen, "Message..", f"Product has been\ndeleted successfully")
            except Exception as ex:
                TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def save_product(screen, sel_prod, pname, ptype, pbuy, psell, pwarehouse, pquantity):
    chosen_wh_name = pwarehouse.split("|")[0].strip()
    chosen_wh = WhServ.get_wh_by_name(chosen_wh_name, DB.warehouses)
    current_quantity = sel_prod.quantity

    # Change quantity and remove/add from/to warehouse
    if int(current_quantity) > int(pquantity):
        # Remove
        amount_to_remove = int(current_quantity) - int(pquantity)
        sel_prod.quantity -= amount_to_remove
        # Remove from warehouse
        WhServ.remove_product(chosen_wh, sel_prod.product_id, amount_to_remove)
        # TODO - log removed amount
    elif int(current_quantity) < int(pquantity):
        # Add
        sel_prod.quantity = int(pquantity)
        # Add to warehouse
        WhServ.add_product(chosen_wh, sel_prod.product_id, sel_prod.quantity)
        # TODO log added amount

    try:
        sel_prod.product_name = pname
        sel_prod.product_type = ptype
        sel_prod.buy_price = pbuy
        sel_prod.sell_price = psell
        sel_prod.assigned_to_wh = chosen_wh.wh_name
        save_products()
        clear_prod_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"Product has been\nchanged successfully")
    except Exception as ex:
        TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")

    # TODO log changed product status


def chose_wh_for_product(screen, choice):
    pass


def on_dropdown_change(screen, var):
    selected_prod_id = var.get().split("-")[0]
    selected_prod = ProdServ.get_product_by_id(selected_prod_id, DB.products)
    # clear_product_properties(screen)

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_edit_prod_name", text="Name:", font=("Arial", 12)) \
        .grid(row=13, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_prod_type", text="Type:", font=("Arial", 12)) \
        .grid(row=15, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_prod_buy", text="Buy Price:", font=("Arial", 12)) \
        .grid(row=13, column=4, sticky="e")
    Label(screen, name="lbl_for_edit_prod_sell", text="Sell Price:", font=("Arial", 12)) \
        .grid(row=11, column=4, sticky="e")
    Label(screen, name="lbl_for_edit_prod_assigned_wh", text="Assigned to:", font=("Arial", 12)) \
        .grid(row=10, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_prod_quantity", text="Quantity:", font=("Arial", 12)) \
        .grid(row=17, column=2, sticky="e")

    # Create Entry fields to edit the product
    pname = Entry(screen, width=30, name="edit_prod_name")
    pname.grid(row=13, column=1, columnspan=2, sticky="w")
    pname.insert(0, selected_prod.product_name)
    buy_price = Entry(screen, width=30, name="edit_prod_buy_price")
    buy_price.insert(0, selected_prod.buy_price)
    buy_price.grid(row=13, column=5, columnspan=4, sticky="w")
    sell_price = Entry(screen, width=30, name="edit_prod_sell_price")
    sell_price.insert(0, selected_prod.sell_price)
    sell_price.grid(row=11, column=5, sticky="w")
    quantity = Entry(screen, width=30, name="edit_prod_quantity")
    quantity.insert(0, selected_prod.quantity)
    quantity.grid(row=17, column=3, columnspan=4, sticky="w")

    # Create DropDown with all existing warehouses
    chosen_wh = StringVar(screen)

    if "none" in selected_prod.assigned_to_wh:
        chosen_wh.set("none")
    else:
        chosen_wh.set(selected_prod.assigned_to_wh)
    chosen_wh_options = ["none"]
    for warehouse in DB.warehouses:
        chosen_wh_options.append(f"{warehouse.wh_name} | Type: {warehouse.wh_type}")

    TkServ.create_drop_down(screen, chosen_wh, chosen_wh_options,
                            lambda a: chose_wh_for_product(screen, chosen_wh), 10, 1, stick="we",
                            cspan=3, padx=(0, 100))

    # Select new user type
    prod_type = StringVar()
    prod_type.set(selected_prod.product_type)
    Radiobutton(screen, text="Finished Goods", variable=prod_type, value="Finished Goods", name="rb_fg") \
        .grid(row=15, column=1, sticky="w")
    Radiobutton(screen, text="Raw Materials", variable=prod_type, value="Raw Materials", name="rb_rm") \
        .grid(row=15, column=1, sticky="e")

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12), bg="lightgreen",
           command=lambda: save_product(screen, selected_prod, pname.get(),
                                        prod_type.get(), buy_price.get(), sell_price.get(), chosen_wh.get(),
                                        quantity.get())) \
        .grid(row=19, column=2, columnspan=4, sticky="w")
    # Create button to delete the selected user
    Button(screen, text="Delete", width=25, name="del_user_btn", font=("Arial", 12), bg="coral",
           command=lambda: delete_product(screen, selected_prod)) \
        .grid(row=6, column=5, columnspan=4, sticky="w")


def create_new_prod(screen, pname, bprice, sprice, ptype, quantity, chosenwh):
    chosen_wh_name = chosenwh.split("|")[0].strip()

    if not quantity.isnumeric():
        TkServ.create_custom_msg(screen, "Warning!", "Invalid product quantity!")
        return

    new_prod_id = ProdServ.get_id_for_new_product(DB.products)
    prod_data = [{
        "product_id": new_prod_id,
        "product_name": pname,
        "product_type": ptype,
        "buy_price": bprice,
        "sell_price": sprice,
        "assigned_to_wh": chosen_wh_name,
        "quantity": quantity
    }]
    status = DB.create_products(prod_data)
    if "Success" in status:
        save_products()
        clear_prod_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"User has been\ncreated successfully")
    else:
        TkServ.create_custom_msg(screen, "Warning!", status)


def new_prod(screen):
    # Clear the screen
    clear_prod_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Creating New Products")

    # Select new product type
    prod_type = StringVar()
    prod_type.set("Finished Goods")
    Radiobutton(screen, text="Finished Goods", variable=prod_type, value="Finished Goods", name="rb_fg") \
        .grid(row=10, column=2, sticky="w")
    Radiobutton(screen, text="Raw Materials", variable=prod_type, value="Raw Materials", name="rb_rm") \
        .grid(row=11, column=2, sticky="w")

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_new_prod_name", text="Name:", font=("Arial", 12)) \
        .grid(row=7, column=1, sticky="ns")
    Label(screen, name="lbl_for_new_prod_type", text="Type:", font=("Arial", 12)) \
        .grid(row=10, rowspan=2, column=1, sticky="e")
    Label(screen, name="lbl_for_new_prod_buy", text="Buy Price:", font=("Arial", 12)) \
        .grid(row=7, column=4, sticky="e")
    Label(screen, name="lbl_for_new_prod_sell", text="Sell Price:", font=("Arial", 12)) \
        .grid(row=11, column=4, sticky="e")
    Label(screen, name="lbl_for_new_prod_quantity", text="Quantity:", font=("Arial", 12)) \
        .grid(row=14, column=2, sticky="e")
    Label(screen, name="lbl_for_new_prod_assig", text="Assign to:", font=("Arial", 12)) \
        .grid(row=16, column=1, sticky="e")

    # Create Entry fields for the new product
    pname = Entry(screen, width=30, name="new_prod_name")
    pname.grid(row=7, column=1, columnspan=2, sticky="e")
    buy_price = Entry(screen, width=30, name="new_prod_buy_price")
    buy_price.grid(row=7, column=5, columnspan=4, sticky="w")
    sell_price = Entry(screen, width=30, name="new_prod_sell_price")
    sell_price.grid(row=11, column=5, columnspan=4, sticky="w")
    quantity = Entry(screen, width=30, name="new_prod_quantity")
    quantity.grid(row=14, column=3, columnspan=4, sticky="w")

    # Create DropDown with all existing warehouses
    chosen_wh = StringVar(screen)
    chosen_wh.set("none")
    chosen_wh_options = ["none"]
    for warehouse in DB.warehouses:
        chosen_wh_options.append(f"{warehouse.wh_name} | Type: {warehouse.wh_type}")

    TkServ.create_drop_down(screen, chosen_wh, chosen_wh_options,
                            lambda a: chose_wh_for_product(screen, chosen_wh), 16, 2, stick="we",
                            cspan=3)

    # Create button to create the product
    Button(screen, text="Save", width=25, name="save_prod_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: create_new_prod(screen, pname.get(), buy_price.get(), sell_price.get(), prod_type.get(),
                                           quantity.get(), chosen_wh.get())) \
        .grid(row=18, column=2, columnspan=4, sticky="w")


def edit_prod(screen):
    # Clear the screen
    clear_prod_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Editing Products")

    # Labels
    Label(screen, text="Product:", font=("Arial", 12)).grid(row=6, column=0, sticky="e")

    # Create DropDown with all existing products
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("Chose a product...")
    drop_down_options = []
    for product in DB.products:
        drop_down_options.append(f"{product.product_id} - "
                                 f"{product.product_name} - "
                                 f"{product.product_type}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_dropdown_change(screen, drop_down_variable), 6, 1, stick="w", cspan=2)
