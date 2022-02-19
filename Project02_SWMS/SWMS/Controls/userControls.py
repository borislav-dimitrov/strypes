import tkinter.messagebox
from tkinter import *
import Models.Db.fakeDB as DB
import Services.tkinterServices as TkServ
import Services.userServices as UsrServ
from Models.Data.saveData import save_users


def clear_usr_screen(screen):
    clear_all_but = [".!toplevel.edit_usr_btn", ".!toplevel.new_usr_btn", ".!toplevel.header_lbl"]
    for widget in screen.grid_slaves():
        if str(widget) not in clear_all_but:
            widget.destroy()


def save_user(screen, user_id, uname, pwd):
    if len(pwd) < 6:
        screen.withdraw()
        TkServ.create_custom_msg(screen, "Warning!", "Chose stronger password!")
    else:
        try:
            selected_user = UsrServ.get_user_by_id(user_id, DB.login_users)
            selected_user.user_name = uname
            selected_user.user_pwd = UsrServ.encrypt_pwd(pwd)
            save_users()
            screen.destroy()
            TkServ.create_msg("Message..", f"User has been changed successfully")
        except Exception as ex:
            TkServ.create_custom_msg(screen, "Warning!", f"Something went wrong!\n{ex}")


def delete_user(screen, user_id):
    curr_user = UsrServ.get_user_by_id(int(user_id), DB.login_users)
    result = tkinter.messagebox.askquestion("Question...",
                                            f"Are you sure you want\nto delete the user\n{curr_user.user_name}",
                                            parent=screen)
    if result == "yes":
        if DB.curr_user == curr_user:
            TkServ.create_custom_msg(screen, "Warning!", "Cannot delete your current user!", w=350)
            return
        u_index = UsrServ.get_user_index_by_id(user_id, DB.login_users)
        if u_index:
            DB.login_users.pop(u_index)
            save_users()


def on_dropdown_change(screen, var):
    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_edit_uname", text="Edit Username:", font=("Arial", 12)) \
        .grid(row=3, column=0, sticky="e")
    Label(screen, name="lbl_for_edit_password", text="Edit Password:", font=("Arial", 12)) \
        .grid(row=3, column=2, sticky="e")
    # Create Entry fields to edit the user
    uname = Entry(screen, width=30, name="edit_user_name")
    uname.grid(row=3, column=1, sticky="w")
    uname.insert(0, var.get().split("-")[1].strip())
    pwd = Entry(screen, width=30, name="edit_user_pwd", show="*")
    pwd.grid(row=3, column=3, sticky="w")

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12), bg="lightgreen",
           command=lambda: save_user(screen, var.get().split("-")[0], uname.get(), pwd.get())) \
        .grid(row=3, column=2, rowspan=2)
    # Create button to delete the selected user
    Button(screen, text="Delete", width=25, name="del_user_btn", font=("Arial", 12), bg="coral",
           command=lambda: delete_user(screen, var.get().split("-")[0])) \
        .grid(row=2, column=3)


def edit_usr(screen):  # , tkinter
    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Editing users")

    # Clear the screen
    clear_usr_screen(screen)

    # Create DropDown with all existing users
    drop_down_variable = tkinter.StringVar(screen)
    drop_down_variable.set("Chose an user...")
    drop_down_options = []
    for user in DB.login_users:
        drop_down_options.append(f"{user.user_id} - {user.user_name}")
    TkServ.create_drop_down(screen, drop_down_variable, drop_down_options,
                            lambda a: on_dropdown_change(screen, drop_down_variable), 2, 1, stick="we")


def create_new_user(screen, uname, pwd, usr_type):
    if len(pwd) < 6:
        screen.withdraw()
        TkServ.create_custom_msg(screen, "Warning!", "Chose stronger password!")
        return
    new_usr_id = UsrServ.get_id_for_new_user(DB.login_users)
    user_data = [{
        "user_id": new_usr_id,
        "user_uname": uname,
        "user_pwd": UsrServ.encrypt_pwd(pwd).decode("utf-8"),
        "user_type": usr_type,
        "user_status": "Active",
        "user_last_login": ""
    }]
    status = DB.create_users(user_data)
    if status == "Success":
        save_users()
        screen.destroy()
        TkServ.create_custom_msg(screen, "Message..", f"User has been changed successfully")
    else:
        TkServ.create_custom_msg(screen, "Warning!", status)


def new_usr(screen):
    # Change the header
    hdr = screen.nametowidget("header_lbl")
    hdr.config(text="Creating new user")

    # Clear the screen
    clear_usr_screen(screen)
    # Create Labels for the Entry fields
    Label(screen, name="lbl_for_new_uname", text="Username:", font=("Arial", 12)) \
        .grid(row=2, column=0, sticky="e")
    Label(screen, name="lbl_for_new_password", text="Password:", font=("Arial", 12)) \
        .grid(row=2, column=2, sticky="e")
    # Create Entry fields to fill info for the new user
    uname = Entry(screen, width=30, name="edit_user_name")
    uname.grid(row=2, column=1, sticky="w")
    pwd = Entry(screen, width=30, name="edit_user_pwd", show="*")
    pwd.grid(row=2, column=3, sticky="w")

    # Select new user type
    usr_type = "Operator"
    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12),
           bg="lightgreen",
           command=lambda: create_new_user(screen, uname.get(), pwd.get(), usr_type)) \
        .grid(row=2, column=2, rowspan=2)
