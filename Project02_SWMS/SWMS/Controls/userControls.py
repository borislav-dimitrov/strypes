from Models.Db.fakeDB import login_users, create_users
from Services.tkinterServices import *
from Services.userServices import *
from Models.Data.saveData import save_users


def save_user(screen, user_id, uname, pwd):
    if len(pwd) < 6:
        screen.withdraw()
        create_custom_warn(screen, "Warning!", "Chose stronger password!")
    else:
        try:
            selected_user = get_user_by_id(user_id, login_users)
            selected_user.user_name = uname
            selected_user.user_pwd = encrypt_pwd(pwd)
            save_users()
            screen.destroy()
            create_msg("Message..", f"User has been changed successfully")
        except Exception as ex:
            create_custom_warn(screen, "Warning!", f"Something went wrong!\n{ex}")


def on_dropdown_change(screen, var):
    # Create Entry fields to edit the user
    uname = Entry(screen, width=30, name="edit_user_name")
    uname.grid(row=3, column=1, columnspan=2, sticky="w")
    uname.insert(0, var.get().split("-")[1].strip())
    pwd = Entry(screen, width=30, name="edit_user_pwd", show="*")
    pwd.grid(row=3, column=2, columnspan=2, sticky="e")

    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12),
           command=lambda: save_user(screen, var.get().split("-")[0], uname.get(), pwd.get())) \
        .grid(row=3, column=2, rowspan=2)


def edit_usr(screen, tkinter):
    # Create DropDown with all existing users
    drop_down_variable = tkinter.StringVar(screen)
    drop_down_variable.set("Chose an user...")
    drop_down_options = []
    for user in login_users:
        drop_down_options.append(f"{user.user_id} - {user.user_name}")
    create_drop_down(screen, drop_down_variable, drop_down_options,
                     lambda a: on_dropdown_change(screen, drop_down_variable), 2, 2, 1, 1, "we")


def create_new_user(screen, uname, pwd, usr_type):
    new_usr_id = get_id_for_new_user(login_users)
    user_data = [{
        "user_id": new_usr_id,
        "user_uname": uname,
        "user_pwd": encrypt_pwd(pwd).decode("utf-8"),
        "user_type": usr_type,
        "user_status": "Active",
        "user_last_login": ""
    }]
    status = create_users(user_data)
    if status == "Success":
        save_users()
        screen.destroy()
        create_custom_msg(screen, "Message..", f"User has been changed successfully")
    else:
        create_custom_msg(screen, "Warning!", status)


def new_usr(screen):
    # Create Labels for the Entry fields
    Label(screen, text="Type in username")
    # Create Entry fields to fill info for the new user
    uname = Entry(screen, width=30, name="edit_user_name")
    uname.grid(row=2, column=1, columnspan=2, sticky="w")
    pwd = Entry(screen, width=30, name="edit_user_pwd", show="*")
    pwd.grid(row=2, column=2, columnspan=2, sticky="e")

    # Select new user type
    usr_type = "Operator"
    # Create button to save the changes
    Button(screen, text="Save", width=25, name="save_user_btn", font=("Arial", 12),
           command=lambda: create_new_user(screen, uname.get(), pwd.get(), usr_type)) \
        .grid(row=2, column=2, rowspan=2)
