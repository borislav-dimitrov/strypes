import tkinter.messagebox
from tkinter import *
import Models.Db.fakeDB as DB
from Models.Data.saveData import save_suppliers
import Services.tkinterServices as TkServ
import Services.suppliersServices as SupServ


def clear_supp_screen(screen):
    clear_all_but = ["edit_supp_btn", "new_supp_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="Create/Modify Suppliers")


def create_new_supplier(screen, sname, sphone, siban, supmenu):
    valid_info, status, items = SupServ.validate_supp_menu(supmenu)
    if not valid_info:
        TkServ.create_custom_msg(screen, "Warning!", status)
        return
    new_supp_id = SupServ.get_id_for_new_supplier(DB.suppliers)
    supp_data = [{
        "supplier_id": new_supp_id,
        "supplier_name": sname,
        "supplier_phone": sphone,
        "supplier_iban": siban,
        "supplier_status": "Active",
        "buy_menu": supmenu
    }]
    status = DB.create_suppliers(supp_data)
    if "Success" in status:
        save_suppliers()
        clear_supp_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"Supplier has been\ncreated successfully")
    else:
        TkServ.create_custom_msg(screen, "Warning!", status)


def new_supplier(screen):
    # Clear the screen
    clear_supp_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Creating New Suppliers")

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_new_supp_name", text="Supplier Name:", font=("Arial", 12)) \
        .grid(row=3, column=0, sticky="e")
    Label(screen, name="lbl_for_new_supp_phone", text="Supplier Phone:", font=("Arial", 12)) \
        .grid(row=4, column=2, sticky="e")
    Label(screen, name="lbl_for_new_supp_iban", text="Supplier IBAN:", font=("Arial", 12)) \
        .grid(row=3, column=2, sticky="e")
    Label(screen, name="lbl_for_new_supp_buy_menu",
          text="Buy Menu pattern: productname-product type-buy price(float)|product...",
          font=("Arial", 13)) \
        .grid(row=5, column=1, columnspan=3, sticky="we")
    Label(screen, name="lbl_for_new_supp_buy_menu2", text="Supplier Buy Menu:", font=("Arial", 12)) \
        .grid(row=6, column=2, sticky="ws")

    # Create Entry fields for the new supplier
    supname = Entry(screen, width=30, name="new_sup_name")
    supname.grid(row=3, column=1)
    supphone = Entry(screen, width=30, name="new_sup_phone")
    supphone.grid(row=4, column=3)
    supiban = Entry(screen, width=30, name="new_sup_iban")
    supiban.grid(row=3, column=3)
    supmenu = Entry(screen, width=30, name="new_sup_buy_menu")
    supmenu.grid(row=7, column=1, columnspan=3, sticky="ew")

    # Create button to create the supplier
    Button(screen, text="Save", width=25, name="save_supplier_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: create_new_supplier(screen, supname.get(), supphone.get(), supiban.get(), supmenu.get())) \
        .grid(row=8, column=2)


def save_supplier(screen, selected_supp, spname, spphone, spiban, spstatus, spmenu):
    try:
        valid_info, status, items = SupServ.validate_supp_menu(spmenu)
        if not valid_info:
            TkServ.create_custom_msg(screen, "Warning!", status)
            return
        selected_supp.supp_name = spname
        selected_supp.supp_phone = spphone
        selected_supp.supp_iban = spiban
        selected_supp.supp_status = spstatus
        selected_supp.buy_menu = spmenu
        save_suppliers()
        clear_supp_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"Supplier has been\nchanged successfully")
    except Exception as ex:
        TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def del_supplier(screen, selected_supp):
    result = tkinter.messagebox.askquestion("Question...",
                                            f"Are you sure you want\n"
                                            f"to delete the supplier\n{selected_supp.supp_name}",
                                            parent=screen)
    if result == "yes":
        u_index = SupServ.get_supp_index_by_id(selected_supp.supp_id, DB.suppliers)
        if u_index:
            try:
                DB.suppliers.pop(u_index)
                save_suppliers()
                clear_supp_screen(screen)
                TkServ.create_custom_msg(screen, "Message..", f"Supplier has been\ndeleted successfully")
            except Exception as ex:
                TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def on_dropdown_change(screen, var):
    selected_supp_id = var.get().split("-")[0]
    selected_supp = SupServ.get_supplier_by_id(selected_supp_id, DB.suppliers)

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_edit_supp_name", text="Supp Name:", font=("Arial", 12)) \
        .grid(row=3, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_supp_phone", text="Supp Phone:", font=("Arial", 12)) \
        .grid(row=3, column=2, sticky="e")
    Label(screen, name="lbl_for_edit_supp_iban", text="Supp IBAN:", font=("Arial", 12)) \
        .grid(row=4, column=2, sticky="e")
    Label(screen, name="lbl_for_edit_supp_status", text="Supp Status:", font=("Arial", 12)) \
        .grid(row=4, column=0, sticky="e")
    Label(screen, name="lbl_for_new_supp_buy_menu",
          text="Buy Menu pattern: productname-product type-buy price(float)|product...",
          font=("Arial", 13)) \
        .grid(row=5, column=1, columnspan=3, sticky="we")
    Label(screen, name="lbl_for_new_supp_buy_menu2", text="Supplier Buy Menu:", font=("Arial", 12)) \
        .grid(row=6, column=2, sticky="wn")

    # Create Entry fields to edit the supplier
    sp_name = Entry(screen, width=30, name="edit_supp_name")
    sp_name.grid(row=3, column=1, sticky="w")
    sp_name.insert(0, selected_supp.supp_name)
    sp_phone = Entry(screen, width=30, name="edit_supp_phone")
    sp_phone.insert(0, selected_supp.supp_phone)
    sp_phone.grid(row=3, column=3, sticky="w")
    sp_iban = Entry(screen, width=30, name="edit_supp_iban")
    sp_iban.insert(0, selected_supp.supp_iban)
    sp_iban.grid(row=4, column=3, sticky="w")
    sp_menu = Entry(screen, width=30, name="new_sup_buy_menu")
    sp_menu.insert(0, selected_supp.buy_menu)
    sp_menu.grid(row=6, column=1, columnspan=3, sticky="ew")
    # Change supplier status
    sp_status = StringVar()
    sp_status.set(selected_supp.supp_status)
    Radiobutton(screen, text="Active", variable=sp_status, value="Active", name="rb_act") \
        .grid(row=4, rowspan=2, column=1, sticky="n")
    Radiobutton(screen, text="Disabled", variable=sp_status, value="Disabled", name="rb_dis") \
        .grid(row=3, rowspan=2, column=1, sticky="s")

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_supp_btn", font=("Arial", 12), bg="lightgreen",
           command=lambda: save_supplier(screen, selected_supp, sp_name.get(),
                                         sp_phone.get(), sp_iban.get(), sp_status.get(), sp_menu.get())) \
        .grid(row=7, column=2, rowspan=2)
    # Create button to delete the selected supplier
    Button(screen, text="Delete", width=25, name="del_supp_btn", font=("Arial", 12), bg="coral",
           command=lambda: del_supplier(screen, selected_supp)) \
        .grid(row=2, column=3)


def edit_supplier(screen):
    # Clear the screen
    clear_supp_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Editing Suppliers")

    # Create DropDown with all existing suppliers
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("Chose a supplier...")
    drop_down_options = []
    for supplier in DB.suppliers:
        drop_down_options.append(f"{supplier.supp_id} - "
                                 f"{supplier.supp_name}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_dropdown_change(screen, drop_down_variable), 2, 1, stick="we")
