import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class MyHome:
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
        self.admin = True

        # region Styles

        # region Buttons
        self.accept_btn_style = ttk.Style()
        self.accept_btn_style.theme_use("alt")

        self.cancel_btn_style = ttk.Style()
        self.cancel_btn_style.theme_use("alt")

        self.normal_btn_style = ttk.Style()
        self.normal_btn_style.theme_use("alt")

        self.accept_btn_style.configure('Green.TButton', background='#98ff61', foreground='black', width=20,
                                        borderwidth=1, font=self.text_bold,
                                        focusthickness=5, focuscolor='red')
        self.accept_btn_style.map('Green.TButton', background=[('active', '#98ff61')])

        self.cancel_btn_style.configure('Red.TButton', background='red', foreground='black', width=10, borderwidth=1,
                                        font=self.text_bold,
                                        focusthickness=5, focuscolor='#98ff61')
        self.cancel_btn_style.map('Red.TButton', background=[('active', 'red')])

        self.normal_btn_style.configure('Normal.TButton', background='#4bb8ff', foreground='black', width=15,
                                        borderwidth=1, font=self.text_bold,
                                        focusthickness=5, focuscolor='#98ff61')
        self.normal_btn_style.map('Normal.TButton', background=[('active', '#4bb8ff')])
        # endregion

        # endregion

        self.m_screen.iconbitmap("./images/main_ico.ico")

        # Set Geometry
        self.m_screen.geometry(f"{self.width}x{self.height}+{int(self.x)}+{int(self.y)}")
        # self.m_screen.resizable(False, False)
        # Set Title
        self.m_screen.title(title)
        # Setup Grid
        self.setup_grid()
        # Create GUI

        # self.bg_img = tk.PhotoImage(file="./images/home/home2.png")
        self.img = Image.open("images/home/home2.png")
        self.img_copy = self.img.copy()

        self.bg_img = ImageTk.PhotoImage(self.img)

        self.canvas = tk.Canvas(self.m_screen, width=self.width, height=self.height)
        self.canvas.grid(row=0, column=0, columnspan=self.grid_cols, rowspan=self.grid_rows, sticky="nsew")
        # Draw BG
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        # Draw Header
        self.canvas.create_text(self.width / 2, 50, text=self.page_name, font=self.heading, fill="white")
        # Draw Labels
        self.canvas.create_text(100, 50, text=f"Hello, user.", font=self.text_bold, fill="white")
        self.canvas.bind("<Configure>", self._redraw_canvas)

        # Logout Btn
        self.btn1 = ttk.Button(self.m_screen, text="Logout", style="Red.TButton")
        self.btn1.grid(row=1, column=self.grid_cols - 4, columnspan=3, sticky="e", padx=(0, 5))

        # Create User Buttons
        self.btn1 = ttk.Button(self.m_screen, text="Warehouses", style="Normal.TButton")
        self.btn1.grid(row=9, column=4, rowspan=2, columnspan=15, sticky="wns")
        self.btn1 = ttk.Button(self.m_screen, text="Purchases", style="Normal.TButton")
        self.btn1.grid(row=9, column=10, rowspan=2, columnspan=15, sticky="wns")
        self.btn1 = ttk.Button(self.m_screen, text="Sales", style="Normal.TButton")
        self.btn1.grid(row=9, column=16, rowspan=2, columnspan=15, sticky="wns")
        self.btn1 = ttk.Button(self.m_screen, text="Transactions", style="Normal.TButton")
        self.btn1.grid(row=9, column=22, rowspan=2, columnspan=15, sticky="wns")

        if self.admin:
            # Create Admin Buttons
            self.btn1 = ttk.Button(self.m_screen, text="User\nManagement", style="Normal.TButton")
            self.btn1.grid(row=17, column=4, rowspan=2, columnspan=15, sticky="wns")
            self.btn1 = ttk.Button(self.m_screen, text="Warehouse\nManagement", style="Normal.TButton")
            self.btn1.grid(row=17, column=10, rowspan=2, columnspan=15, sticky="wns")
            self.btn1 = ttk.Button(self.m_screen, text="Product\nManagement", style="Normal.TButton")
            self.btn1.grid(row=17, column=16, rowspan=2, columnspan=15, sticky="wns")
            self.btn1 = ttk.Button(self.m_screen, text="Supplier\nManagement", style="Normal.TButton")
            self.btn1.grid(row=17, column=22, rowspan=2, columnspan=15, sticky="wns")
            self.btn1 = ttk.Button(self.m_screen, text="Client\nManagement", style="Normal.TButton")
            self.btn1.grid(row=21, column=4, rowspan=2, columnspan=15, sticky="wns")
            self.btn1 = ttk.Button(self.m_screen, text="Invoice\nManagement", style="Normal.TButton")
            self.btn1.grid(row=21, column=10, rowspan=2, columnspan=15, sticky="wns")

    def _redraw_canvas(self, event):
        new_width = event.width
        new_height = event.height

        self.img = self.img_copy.resize((new_width, new_height))
        self.bg_img = ImageTk.PhotoImage(self.img)
        self.canvas.delete("all")

        # Draw BG
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        # Draw Header
        self.canvas.create_text(new_width / 2, 50, text=self.page_name, font=self.heading, fill="white")
        # Draw Labels
        self.canvas.create_text(100, 50, text=f"Hello, user.", font=self.text_bold, fill="white")

    def setup_grid(self):
        # set rows
        for row in range(self.grid_rows):
            tk.Grid.rowconfigure(self.m_screen, row, weight=1)
            # self.m_screen.grid_rowconfigure(row, minsize=self.height / self.grid_rows)

        # set columns
        for col in range(self.grid_cols):
            tk.Grid.columnconfigure(self.m_screen, col, weight=1)
            # self.m_screen.grid_columnconfigure(col, minsize=self.width / self.grid_cols)
