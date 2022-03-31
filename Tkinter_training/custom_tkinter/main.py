import tkinter as tk
import customtkinter as ctk
from ctk_class import MyCustomTkinter
from custom_tkinter.login import MyCtkLogin
from custom_tkinter.home import MyHome
from custom_tkinter.user_mgmt_view import UserManagement
import theme_cfg as cfg


def main():
    # region SETUP THEME
    if cfg._THEME == "Light":
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")
    elif cfg._THEME == "Dark":
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    # endregion

    # root = ctk.CTk()
    # login = MyCtkLogin(root, "Login", (640, 360), grid_rows=6, grid_cols=10)
    # root.mainloop()

    root = ctk.CTk()
    home = MyHome(root, "Home", (1280, 720))
    root.mainloop()

    # root = ctk.CTk()
    # user_mgmt = UserManagement(root, "User Management", (1280, 720))
    # root.mainloop()


if __name__ == '__main__':
    main()
