import tkinter as tk
from tkinter import ttk
import Model.Modules.all_modules as Modules
import Model.DataBase.my_db as db
import Helpers.tk_helpers as tkhlp


class MyLogin:
    def __init__(self, m_screen, page_name, title, width, height, grid_rows, grid_cols):
        self.m_screen = m_screen
        self.page_name = page_name
        self.title = title
        self.width = width
        self.height = height
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.x = (self.m_screen.winfo_screenwidth() / 2) - (self.width / 2)
        self.y = (self.m_screen.winfo_screenheight() / 2) - (self.height / 2)
        self.text = ("Arial", 12)
        self.text_bold = ("Arial", 12, "bold")
        self.heading = ("Arial", 15, "bold")

        # region Styles

        # region Buttons
        self.accept_btn_style = ttk.Style()
        self.accept_btn_style.theme_use("alt")

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.theme_use("alt")

        self.accept_btn_style.configure('Green.TButton', background='#98ff61', foreground='black', width=20,
                                        borderwidth=1, font=self.text_bold,
                                        focusthickness=5, focuscolor='red')
        self.accept_btn_style.map('Green.TButton', background=[('active', '#98ff61')])

        self.cancel_btn_style.configure('Red.TButton', background='red', foreground='black', width=20, borderwidth=1,
                                        font=self.text_bold,
                                        focusthickness=5, focuscolor='#98ff61')
        self.cancel_btn_style.map('Red.TButton', background=[('active', 'red')])
        # endregion

        # endregion

        self.m_screen.iconbitmap("./Resources/images/login/login_ico.ico")
        # Set Geometry
        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        self.m_screen.resizable(False, False)
        # Set Title
        self.m_screen.title(title)
        # Setup Grid
        tkhlp.setup_grid(self.m_screen, self.grid_rows, self.grid_cols, self.height, self.width)
        # Create GUI
        self.bg_img = tk.PhotoImage(file=r"./Resources/images/login/login3.png")
        self.canvas = tk.Canvas(self.m_screen, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, columnspan=self.grid_cols, rowspan=self.grid_rows, sticky="nesw")
        # Draw BG
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        # Draw Header
        self.canvas.create_text(self.width / 2, 120, text=self.page_name, font=self.heading, fill="white")
        # Draw Labels
        self.canvas.create_text(230, 180, text="Username :", font=self.text_bold, fill="white")
        self.canvas.create_text(230, 215, text="Password :", font=self.text_bold, fill="white")

        # Create Entry Fields
        self.uname_entry = ttk.Entry(self.m_screen)
        self.uname_entry.grid(row=13, column=10, columnspan=8, sticky="we")
        self.pwd_entry = ttk.Entry(self.m_screen, show="*")
        self.pwd_entry.grid(row=15, column=10, columnspan=8, sticky="we")

        # Create Buttons
        self.login_btn = ttk.Button(self.m_screen, text="Login", style="Green.TButton",
                                    command=lambda: self.login())
        self.login_btn.grid(row=19, column=7, columnspan=5, sticky="w")
        self.cancel_btn = ttk.Button(self.m_screen, text="Cancel", style="Red.TButton",
                                     command=lambda: self.cancel())
        self.cancel_btn.grid(row=19, column=13, columnspan=5, sticky="w")

        self.m_screen.protocol("WM_DELETE_WINDOW", lambda: self.on_exit())

    def login(self):
        user = Modules.umgmt.verify_user(self.uname_entry.get(), self.pwd_entry.get())
        if user != "Unauthorized":
            db.curr_user = user
            self.m_screen.destroy()
        else:
            print("Invalid username/password!")
            # TODO Message

    def cancel(self):
        self.on_exit()

    def on_exit(self):
        self.m_screen.destroy()
        quit()
