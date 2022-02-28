import tkinter.messagebox
from tkinter import *
import Models.Db.fakeDB as DB
import Services.clientServices as CliServ
from Models.Data.saveData import save_clients
import Services.tkinterServices as TkServ


def clear_client_screen(screen):
    clear_all_but = ["edit_client_btn", "new_client_btn", "header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget).split(".").pop() not in clear_all_but:
            widget.destroy()
        if str(widget).split(".").pop() == "header_lbl":
            widget.config(text="Create/Modify Clients")


def create_new_client(screen, client_name, client_phone, client_iban):
    new_client_id = CliServ.get_id_for_new_client(DB.clients)
    client_data = [{
        "client_id": new_client_id,
        "client_name": client_name,
        "client_phone": client_phone,
        "client_iban": client_iban,
        "client_status": "Active"
    }]
    status = DB.create_clients(client_data)
    if "Success" in status:
        save_clients()
        clear_client_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"Client has been created successfully")
    else:
        TkServ.create_custom_msg(screen, "Warning!", status)


def new_client(screen):
    # Clear the screen
    clear_client_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Creating New Client")

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_new_client_name", text="Client Name:", font=("Arial", 12)) \
        .grid(row=7, column=2, sticky="e")
    Label(screen, name="lbl_for_new_client_phone", text="Client Phone:", font=("Arial", 12)) \
        .grid(row=9, column=2, sticky="e")
    Label(screen, name="lbl_for_new_client_iban", text="Client IBAN:", font=("Arial", 12)) \
        .grid(row=11, column=2, sticky="e")

    # Create Entry fields for the new supplier
    client_name = Entry(screen, width=30, name="new_client_name")
    client_name.grid(row=7, column=3, columnspan=2)
    client_phone = Entry(screen, width=30, name="new_client_phone")
    client_phone.grid(row=9, column=3, columnspan=2)
    client_iban = Entry(screen, width=30, name="new_client_iban")
    client_iban.grid(row=11, column=3, columnspan=2)

    # Create button to create the supplier
    Button(screen, text="Save", width=25, name="save_client_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: create_new_client(screen, client_name.get(), client_phone.get(), client_iban.get())) \
        .grid(row=15, column=2, columnspan=4, sticky="w")


def save_client(screen, selected_client, client_name, client_phone, client_iban, client_status):
    try:
        selected_client.client_name = client_name
        selected_client.client_phone = client_phone
        selected_client.client_iban = client_iban
        selected_client.client_status = client_status
        save_clients()
        clear_client_screen(screen)
        TkServ.create_custom_msg(screen, "Message..", f"Client has been\nchanged successfully")
    except Exception as ex:
        TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def delete_client(screen, selected_client):
    result = tkinter.messagebox.askquestion("Question...",
                                            f"Are you sure you want\n"
                                            f"to delete the client\n{selected_client.client_name}",
                                            parent=screen)
    if result == "yes":
        client_index = CliServ.get_client_index_by_id(selected_client.client_id, DB.clients)
        if client_index:
            try:
                DB.clients.pop(client_index)
                save_clients()
                clear_client_screen(screen)
                TkServ.create_custom_msg(screen, "Message..", f"Client has been\ndeleted successfully")
            except Exception as ex:
                TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def on_dropdown_change(screen, var):
    selected_client_id = var.get().split("-")[0]
    selected_client = CliServ.get_client_by_id(selected_client_id, DB.clients)

    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_edit_client_name", text="Client Name:", font=("Arial", 12)) \
        .grid(row=10, column=1, sticky="w")
    Label(screen, name="lbl_for_edit_client_phone", text="Client Phone:", font=("Arial", 12)) \
        .grid(row=10, column=4, sticky="e")
    Label(screen, name="lbl_for_edit_client_iban", text="Client IBAN:", font=("Arial", 12)) \
        .grid(row=12, column=1, sticky="w")
    Label(screen, name="lbl_for_edit_client_status", text="Client Status:", font=("Arial", 12)) \
        .grid(row=12, column=4, sticky="e")

    # Create Entry fields to edit the client
    client_name = Entry(screen, width=30, name="edit_client_name")
    client_name.grid(row=10, column=1, columnspan=3, sticky="w", padx=(100, 0))
    client_name.insert(0, selected_client.client_name)
    client_phone = Entry(screen, width=30, name="edit_client_phone")
    client_phone.insert(0, selected_client.client_phone)
    client_phone.grid(row=10, column=5, columnspan=4, sticky="w")
    client_iban = Entry(screen, width=30, name="edit_client_iban")
    client_iban.insert(0, selected_client.client_iban)
    client_iban.grid(row=12, column=1, columnspan=3, sticky="w", padx=(100, 0))

    # Change client status
    client_status = StringVar()
    client_status.set(selected_client.client_status)
    Radiobutton(screen, text="Active", variable=client_status, value="Active", name="rb_act") \
        .grid(row=12, rowspan=2, column=5, sticky="n")
    Radiobutton(screen, text="Disabled", variable=client_status, value="Disabled", name="rb_dis") \
        .grid(row=12, rowspan=2, column=5, sticky="s")

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_client_btn", font=("Arial", 12), bg="lightgreen",
           command=lambda: save_client(screen, selected_client, client_name.get(),
                                       client_phone.get(), client_iban.get(), client_status.get())) \
        .grid(row=15, column=2, columnspan=4, sticky="w")
    # Create button to delete the selected user
    Button(screen, text="Delete", width=25, name="del_client_btn", font=("Arial", 12), bg="coral",
           command=lambda: delete_client(screen, selected_client)) \
        .grid(row=7, column=5, columnspan=4, sticky="w")


def edit_client(screen):
    # Clear the screen
    clear_client_screen(screen)

    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Editing Clients")

    # Labels
    Label(screen, text="Client:", font=("Arial", 12)).grid(row=7, column=0, sticky="e")

    # Create DropDown with all existing clients
    drop_down_variable = StringVar(screen)
    drop_down_variable.set("Chose a client...")
    drop_down_options = []
    for client in DB.clients:
        drop_down_options.append(f"{client.client_id} - "
                                 f"{client.client_name}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_dropdown_change(screen, drop_down_variable), 7, 1, stick="we")
