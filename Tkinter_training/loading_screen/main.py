import tkinter as tk
import customtkinter as ctk

from loading_screen.loading import Loading


def main():
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    loading = Loading(root, (640, 360))
    root.mainloop()


if __name__ == '__main__':
    main()
