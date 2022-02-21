import tkinter.messagebox
from tkinter import *
import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
import Services.productServices as ProdServ
from Models.Data.saveData import save_products


def clear_prod_screen(screen):
    clear_all_but = ["edit_prod_btn", "new_prod_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="Create/Modify Products")


def delete_product(screen, sel_prod):
    result = tkinter.messagebox.askquestion("Question...",
                                            f"Are you sure you want\nto delete the user\n{sel_prod.product_name}",
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


def save_product(screen, sel_prod, pname, ptype, pbuy, psell):
    try:
        sel_prod.product_name = pname
        sel_prod.product_type = ptype
        sel_prod.buy_price = pbuy
        sel_prod.sell_price = psell
        save_products()
        clear_prod_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"Product has been\nchanged successfully")
    except Exception as ex:
        TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def on_dropdown_change(screen, var):
    selected_prod_id = var.get().split("-")[0]
    selected_prod = ProdServ.get_product_by_id(selected_prod_id, DB.products)
    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_edit_prod_name", text="Name:", font=("Arial", 12)) \
        .grid(row=3, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_prod_type", text="Type:", font=("Arial", 12)) \
        .grid(row=4, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_prod_buy", text="Buy Price:", font=("Arial", 12)) \
        .grid(row=3, column=2, sticky="e")
    Label(screen, name="lbl_for_edit_prod_sell", text="Sell Price:", font=("Arial", 12)) \
        .grid(row=4, column=2, sticky="e")
    # Create Entry fields to edit the product
    pname = Entry(screen, width=30, name="edit_prod_name")
    pname.grid(row=3, column=1, sticky="w")
    pname.insert(0, selected_prod.product_name)
    buy_price = Entry(screen, width=30, name="edit_prod_buy_price")
    buy_price.insert(0, selected_prod.buy_price)
    buy_price.grid(row=3, column=3, sticky="w")
    sell_price = Entry(screen, width=30, name="edit_prod_sell_price")
    sell_price.insert(0, selected_prod.sell_price)
    sell_price.grid(row=4, column=3, sticky="w")

    # Select new user type
    prod_type = StringVar()
    prod_type.set(selected_prod.product_type)
    Radiobutton(screen, text="Finished Goods", variable=prod_type, value="Finished Goods", name="rb_fg") \
        .grid(row=3, rowspan=2, column=1, sticky="s")
    Radiobutton(screen, text="Raw Materials", variable=prod_type, value="Raw Materials", name="rb_rm") \
        .grid(row=4, rowspan=2, column=1, sticky="n")

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12), bg="lightgreen",
           command=lambda: save_product(screen, selected_prod, pname.get(),
                                        prod_type.get(), buy_price.get(), sell_price.get())) \
        .grid(row=5, column=2, rowspan=2)
    # Create button to delete the selected user
    Button(screen, text="Delete", width=25, name="del_user_btn", font=("Arial", 12), bg="coral",
           command=lambda: delete_product(screen, selected_prod)) \
        .grid(row=2, column=3)


def create_new_prod(screen, pname, bprice, sprice, ptype):
    new_prod_id = ProdServ.get_id_for_new_product(DB.products)
    prod_data = [{
        "product_id": new_prod_id,
        "product_name": pname,
        "product_type": ptype,
        "buy_price": bprice,
        "sell_price": sprice
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
        .grid(row=4, column=1, sticky="s")
    Radiobutton(screen, text="Raw Materials", variable=prod_type, value="Raw Materials", name="rb_rm") \
        .grid(row=5, column=1, sticky="n")

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_new_prod_name", text="Name:", font=("Arial", 12)) \
        .grid(row=3, column=0, sticky="e")
    Label(screen, name="lbl_for_new_prod_type", text="Type:", font=("Arial", 12)) \
        .grid(row=4, column=0, sticky="e")
    Label(screen, name="lbl_for_new_prod_buy", text="Buy Price:", font=("Arial", 12)) \
        .grid(row=3, column=2, sticky="e")
    Label(screen, name="lbl_for_new_prod_sell", text="Sell Price:", font=("Arial", 12)) \
        .grid(row=4, column=2, sticky="e")

    # Create Entry fields for the new product
    pname = Entry(screen, width=30, name="new_prod_name")
    pname.grid(row=3, column=1, sticky="w")
    buy_price = Entry(screen, width=30, name="new_prod_buy_price")
    buy_price.grid(row=3, column=3, sticky="w")
    sell_price = Entry(screen, width=30, name="new_prod_sell_price")
    sell_price.grid(row=4, column=3, sticky="w")

    # Create button to create the product
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: create_new_prod(screen, pname.get(), buy_price.get(), sell_price.get(), prod_type.get())) \
        .grid(row=5, column=2)


def edit_prod(screen):
    # Clear the screen
    clear_prod_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Editing Products")

    # Create DropDown with all existing users
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("Chose a product...")
    drop_down_options = []
    for product in DB.products:
        drop_down_options.append(f"{product.product_id} - "
                                 f"{product.product_name} - "
                                 f"{product.product_type}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_dropdown_change(screen, drop_down_variable), 2, 1, stick="we")
