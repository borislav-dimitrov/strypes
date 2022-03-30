import tkinter as tk
import customtkinter as ctk
from ctk_class import MyCustomTkinter
from custom_tkinter.login import MyCtkLogin


def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    # main_win = MyCustomTkinter(root, (1280, 768))
    login = MyCtkLogin(root, "Login", "Login", (640, 360), grid_rows=6, grid_cols=10)
    root.mainloop()


if __name__ == '__main__':
    main()
