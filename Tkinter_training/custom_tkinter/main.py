import tkinter as tk
import customtkinter as ctk
from ctk_class import MyCustomTkinter
from custom_tkinter.login import MyCtkLogin
from custom_tkinter.home import MyHome
from custom_tkinter.user_mgmt_view import UserManagement


def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    # login = MyCtkLogin(root, "Login", (640, 360), grid_rows=6, grid_cols=10)
    # home = MyHome(root, "Home", (1280, 720))
    user_mgmt = UserManagement(root, "User Management", (1280, 720))
    root.mainloop()


if __name__ == '__main__':
    main()
