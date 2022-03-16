from tkinter import *
import tkinter.messagebox
import Services.warehouseServices as WhServ
import Services.tkinterServices as TkServ
import Models.Db.fakeDB as DB


def clear_wh_screen(screen):
    clear_all_but = ["edit_wh_btn", "new_wh_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="Create/Modify Warehouses")


def create_new_wh(screen, wh_name, wh_type, wh_capacity, wh_status):
    new_wh_id = WhServ.get_id_for_new_wh(DB.warehouses)
    wh_data = [{
        "wh_id": new_wh_id,
        "wh_name": wh_name,
        "wh_type": wh_type,
        "wh_capacity": int(wh_capacity),
        "wh_stored": [],
        "wh_status": wh_status
    }]
    status = DB.create_warehouses(wh_data)
    if "Success" in status:
        DB.save_all_data()
        DB.load_all_entities()
        clear_wh_screen(screen)
        DB.my_logger.log(__file__, f"Created warehouse {wh_name}", "INFO")
        TkServ.create_custom_msg(screen, "Message..", f"Warehouse has been created successfully")
    else:
        TkServ.create_custom_msg(screen, "Warning!", status)


def new_wh(screen):
    # Clear the screen
    clear_wh_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Creating New Warehouse")

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_new_wh_name", text="Warehouse Name:", font=("Arial", 12)) \
        .grid(row=7, column=1, columnspan=2, sticky="e")
    Label(screen, name="lbl_for_new_wh_iban", text="Warehouse Capacity:", font=("Arial", 12)) \
        .grid(row=9, column=1, columnspan=2, sticky="e")
    Label(screen, name="lbl_for_new_wh_phone", text="Warehouse Type:", font=("Arial", 12)) \
        .grid(row=12, column=1, columnspan=2, sticky="w")
    Label(screen, name="lbl_for_new_wh_status", text="Warehouse Status:", font=("Arial", 12)) \
        .grid(row=12, column=3, columnspan=2, sticky="w")

    # Select new warehouse Status
    wh_status = StringVar()
    wh_status.set("Active")
    Radiobutton(screen, text="Active", variable=wh_status, value="Active", name="rb_active") \
        .grid(row=11, rowspan=2, column=1, columnspan=2, sticky="w", padx=(150, 0))
    Radiobutton(screen, text="Disabled", variable=wh_status, value="Disabled", name="rb_disable") \
        .grid(row=12, rowspan=2, column=1, columnspan=2, sticky="w", padx=(150, 0))

    # Select new warehouse Type
    wh_type = StringVar()
    wh_type.set("Finished Goods")
    Radiobutton(screen, text="Finished Goods", variable=wh_type, value="Finished Goods", name="rb_fg") \
        .grid(row=11, rowspan=2, column=4, columnspan=2, sticky="w", padx=(60, 0))
    Radiobutton(screen, text="Raw Materials", variable=wh_type, value="Raw Materials", name="rb_rm") \
        .grid(row=12, rowspan=2, column=4, columnspan=2, sticky="w", padx=(60, 0))

    # Create Entry fields for the new supplier
    wh_name = Entry(screen, width=30, name="new_wh_name")
    wh_name.grid(row=7, column=3, columnspan=3, sticky="w")
    # wh_type = Entry(screen, width=30, name="new_wh_type")
    # wh_type.grid(row=9, column=3, columnspan=3, sticky="w")
    wh_capacity = Entry(screen, width=30, name="new_wh_capacity")
    wh_capacity.grid(row=9, column=3, columnspan=3, sticky="w")

    # Create button to create the supplier
    Button(screen, text="Save", width=25, name="save_wh_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: create_new_wh(screen, wh_name.get(), wh_type.get(), wh_capacity.get(), wh_status.get())) \
        .grid(row=15, column=2, columnspan=4, sticky="w")


def delete_wh(screen, selected_wh):
    result = tkinter.messagebox.askquestion("Question...",
                                            f"Are you sure you want\n"
                                            f"to delete the client\n{selected_wh.wh_name}",
                                            parent=screen)
    if result == "yes":
        wh_index = WhServ.get_wh_index_by_id(selected_wh.wh_id, DB.warehouses)
        if wh_index:
            try:
                name = selected_wh.wh_name
                DB.warehouses.pop(wh_index)
                DB.save_all_data()
                DB.load_all_entities()
                clear_wh_screen(screen)
                DB.my_logger.log(__file__, f"Deleted warehouse {name}", "INFO")
                TkServ.create_custom_msg(screen, "Message..", f"Warehouse has been\ndeleted successfully")
            except Exception as ex:
                TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def save_wh(screen, selected_wh, wh_name, wh_type, wh_capacity, wh_status):
    try:
        selected_wh.wh_name = wh_name
        selected_wh.wh_type = wh_type
        selected_wh.wh_capacity = wh_capacity
        selected_wh.wh_status = wh_status
        DB.save_all_data()
        DB.load_all_entities()
        clear_wh_screen(screen)
        DB.my_logger.log(__file__, f"Created/modified warehouse {selected_wh.wh_name}", "INFO")
        TkServ.create_custom_msg(screen, "Message..", f"Warehouse has been\nchanged successfully")
    except Exception as ex:
        TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def on_dropdown_change(screen, var):
    selected_wh_id = var.get().split("-")[0]
    selected_wh = WhServ.get_wh_by_id(selected_wh_id, DB.warehouses)

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_edit_wh_name", text="Warehouse Name:", font=("Arial", 12)) \
        .grid(row=9, column=0, columnspan=2, sticky="w")
    Label(screen, name="lbl_for_edit_w_status", text="Warehouse Status:", font=("Arial", 12)) \
        .grid(row=11, column=0, columnspan=2, sticky="w")
    Label(screen, name="lbl_for_edit_wh_type", text="Warehouse Type:", font=("Arial", 12)) \
        .grid(row=11, column=3, columnspan=2, sticky="w")
    Label(screen, name="lbl_for_edit_wh_capacity", text="Warehouse Capacity:", font=("Arial", 12)) \
        .grid(row=9, column=3, columnspan=2, sticky="w")
    Label(screen, name="lbl_for_edit_wh_free_space", text=f"Free: {WhServ.get_wh_free_space(selected_wh)}",
          font=("Arial", 12)) \
        .grid(row=9, column=5, columnspan=2, sticky="w", padx=(170, 0))

    # Create Entry fields to edit the supplier
    wh_name = Entry(screen, width=30, name="edit_wh_name")
    wh_name.grid(row=9, column=1, columnspan=2, sticky="w", padx=(50, 0))
    wh_name.insert(0, selected_wh.wh_name)
    wh_capacity = Entry(screen, width=30, name="edit_wh_capacity")
    wh_capacity.insert(0, selected_wh.wh_capacity)
    wh_capacity.grid(row=9, column=4, columnspan=2, sticky="w", padx=(80, 0))

    # Change supplier status
    wh_status = StringVar()
    wh_status.set(selected_wh.wh_status)
    Radiobutton(screen, text="Active", variable=wh_status, value="Active", name="rb_act") \
        .grid(row=11, rowspan=2, column=1, sticky="nw", padx=(80, 0))
    Radiobutton(screen, text="Disabled", variable=wh_status, value="Disabled", name="rb_dis") \
        .grid(row=11, rowspan=2, column=1, sticky="sw", padx=(80, 0))

    # Select new warehouse Type
    wh_type = StringVar()
    wh_type.set(str(selected_wh.wh_type))
    Radiobutton(screen, text="Finished Goods", variable=wh_type, value="Finished Goods", name="rb_fg") \
        .grid(row=11, rowspan=2, column=4, columnspan=2, sticky="nw", padx=(60, 0))
    Radiobutton(screen, text="Raw Materials", variable=wh_type, value="Raw Materials", name="rb_rm") \
        .grid(row=11, rowspan=2, column=4, columnspan=2, sticky="sw", padx=(60, 0))

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_wh_btn", font=("Arial", 12), bg="lightgreen",
           command=lambda: save_wh(screen, selected_wh, wh_name.get(),
                                   wh_type.get(), wh_capacity.get(), wh_status.get())) \
        .grid(row=15, column=2, columnspan=4, sticky="w")
    # Create button to delete the selected user
    Button(screen, text="Delete", width=25, name="del_wh_btn", font=("Arial", 12), bg="coral",
           command=lambda: delete_wh(screen, selected_wh)) \
        .grid(row=7, column=5, columnspan=4, sticky="w")


def edit_wh(screen):
    # Clear the screen
    clear_wh_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Editing Warehouses")

    # Labels
    Label(screen, text="Warehouse:", font=("Arial", 12)).grid(row=7, column=0, columnspan=2, sticky="w")

    # Create DropDown with all existing warehouses
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("Chose a warehouse...")
    drop_down_options = []
    for warehouse in DB.warehouses:
        drop_down_options.append(f"{warehouse.wh_id} - "
                                 f"{warehouse.wh_name}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_dropdown_change(screen, drop_down_variable), 7, 1, stick="we")
